const { createApp, ref, computed } = Vue;

const API_BASE = 'http://127.0.0.1:8000';

createApp({
    setup() {
        // 状态
        const currentView = ref('login');
        const currentUser = ref(null);
        const token = ref(localStorage.getItem('token'));

        // 表单数据
        const loginForm = ref({ username: '', password: '' });
        const registerForm = ref({ username: '', password: '', can_create_module: false });

        // 模组数据
        const modules = ref([]);
        const currentModule = ref(null);
        const resources = ref([]);

        // 资源表单
        const showResourceForm = ref(false);
        const newResource = ref({ type: 'text', title: '', content: '', display_type: 'story' });
        const selectedFile = ref(null);

        // 房间数据
        const rooms = ref([]);
        const allRooms = ref([]);
        const allModules = ref([]);
        const filterModuleId = ref(null);
        const gmRooms = ref([]);

        // 新建房间
        const showModuleSelect = ref(false);
        const selectedModuleId = ref(null);

        // 游戏房间数据
        const currentRoom = ref(null);
        const roomResources = ref([]);
        const roomCharacters = ref([]);
        const gameLogs = ref([]);
        const isGM = ref(false);

        // 掷骰子
        const selectedDice = ref(null);
        const diceModifier = ref(0);
        const diceResult = ref(null);

        // 角色卡
        const showCharacterForm = ref(false);
        const editingCharacter = ref(null);
        const characterForm = ref({
            name: '',
            hp: 1,
            max_hp: 1,
            attack_bonus: 1,
            damage_dice: '1d6',
            notes: ''
        });

        // 攻击结果
        const attackResult = ref(null);

        // 日志容器引用
        const logContainer = ref(null);

        // 当前用户的角色
        const myCharacter = computed(() => {
            return roomCharacters.value.find(c => c.user_id === currentUser.value?.id);
        });

        // 判断当前用户是否是 GM
        const checkIsGM = () => {
            if (currentRoom.value && currentUser.value) {
                isGM.value = currentRoom.value.gm_id === currentUser.value.id;
            }
        };

        // ============ 房间游戏相关 ============

        async function joinRoom(room) {
            try {
                const resp = await axios.post(`${API_BASE}/api/rooms/${room.id}/join`, {}, { headers: authHeaders() });
                currentRoom.value = resp.data;
                currentView.value = 'game';
                checkIsGM();
                // 加载房间数据
                loadRoomData(room.id);
                // 启动日志轮询
                startLogPolling(room.id);
            } catch (e) {
                showAlert('加入失败', e.response?.data?.detail || e.message);
            }
        }

        async function fetchRoomDetails(roomId) {
            try {
                const resp = await axios.get(`${API_BASE}/api/rooms/${roomId}`, { headers: authHeaders() });
                // 更新 currentRoom 的详细信息
                if (currentRoom.value && currentRoom.value.id === roomId) {
                    currentRoom.value = { ...currentRoom.value, ...resp.data };
                }
                return resp.data;
            } catch (e) {
                console.error('获取房间详情失败', e);
                return null;
            }
        }

        async function loadRoomData(roomId) {
            await Promise.all([
                fetchRoomDetails(roomId),
                fetchRoomResources(roomId),
                fetchRoomCharacters(roomId),
                fetchGameLogs(roomId)
            ]);
        }

        async function fetchRoomResources(roomId) {
            try {
                const resp = await axios.get(`${API_BASE}/api/rooms/${roomId}/resources`, { headers: authHeaders() });
                roomResources.value = resp.data;
            } catch (e) {
                console.error('获取房间资源失败', e);
            }
        }

        async function fetchRoomCharacters(roomId) {
            try {
                const resp = await axios.get(`${API_BASE}/api/rooms/${roomId}/characters`, { headers: authHeaders() });
                roomCharacters.value = resp.data;
            } catch (e) {
                console.error('获取角色卡失败', e);
            }
        }

        async function fetchGameLogs(roomId) {
            try {
                const resp = await axios.get(`${API_BASE}/api/rooms/${roomId}/logs`, { headers: authHeaders() });
                gameLogs.value = resp.data;
                // 自动滚动到底部
                setTimeout(() => {
                    if (logContainer.value) {
                        logContainer.value.scrollTop = logContainer.value.scrollHeight;
                    }
                }, 100);
            } catch (e) {
                console.error('获取游戏日志失败', e);
            }
        }

        let logPollingInterval = null;

        function startLogPolling(roomId) {
            // 停止之前的轮询
            if (logPollingInterval) {
                clearInterval(logPollingInterval);
            }
            // 每3秒刷新一次日志
            logPollingInterval = setInterval(() => {
                fetchGameLogs(roomId);
                // 同时刷新角色卡（HP可能变化）
                fetchRoomCharacters(roomId);
            }, 3000);
        }

        function stopLogPolling() {
            if (logPollingInterval) {
                clearInterval(logPollingInterval);
                logPollingInterval = null;
            }
        }

        async function leaveRoom() {
            if (currentRoom.value) {
                try {
                    await axios.post(`${API_BASE}/api/rooms/${currentRoom.value.id}/leave`, {}, { headers: authHeaders() });
                } catch (e) {
                    console.error('离开房间失败', e);
                }
            }
            stopLogPolling();
            currentRoom.value = null;
            roomResources.value = [];
            roomCharacters.value = [];
            gameLogs.value = [];
            isGM.value = false;
            currentView.value = 'rooms';
        }

        async function rollDice() {
            if (!selectedDice.value) return;

            try {
                const resp = await axios.post(
                    `${API_BASE}/api/rooms/${currentRoom.value.id}/dice`,
                    {
                        dice: "1d" + selectedDice.value,
                        reason: ""
                    },
                    { headers: authHeaders() }
                );
                diceResult.value = resp.data;
                // 刷新日志
                fetchGameLogs(currentRoom.value.id);
            } catch (e) {
                showAlert('掷骰失败', e.response?.data?.detail || e.message);
            }
        }

        async function quickAttack() {
            if (!myCharacter.value) {
                showAlert('提示', '请先创建角色卡');
                return;
            }

            try {
                const resp = await axios.post(
                    `${API_BASE}/api/characters/${myCharacter.value.id}/attack`,
                    {},
                    { headers: authHeaders() }
                );
                attackResult.value = resp.data.message || `造成 ${resp.data.damage} 点伤害！`;
                // 刷新日志和角色卡
                fetchGameLogs(currentRoom.value.id);
                fetchRoomCharacters(currentRoom.value.id);
            } catch (e) {
                showAlert('攻击失败', e.response?.data?.detail || e.message);
            }
        }

        async function toggleResourceVisibility(resource) {
            try {
                await axios.post(
                    `${API_BASE}/api/rooms/${currentRoom.value.id}/resources/${resource.id}/toggle`,
                    { is_shown: !resource.is_shown },
                    { headers: { ...authHeaders(), 'Content-Type': 'application/json' } }
                );
                fetchRoomResources(currentRoom.value.id);
            } catch (e) {
                showAlert('操作失败', e.response?.data?.detail || e.message);
            }
        }

        function handleImageError(e) {
            e.target.style.display = 'none';
        }

        function getDisplayTypeLabel(type) {
            const labels = {
                story: '背景故事',
                rule: '规则说明',
                clue: '线索卡',
                character: '角色描述',
                mission: '任务目标'
            };
            return labels[type] || type;
        }

        function formatTime(dateStr) {
            if (!dateStr) return '';
            const date = new Date(dateStr);
            return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
        }

        // ============ 角色卡相关 ============

        function editCharacter(character) {
            editingCharacter.value = character;
            characterForm.value = {
                name: character.name,
                hp: character.hp,
                max_hp: character.max_hp,
                attack_bonus: character.attack_bonus,
                damage_dice: character.damage_dice,
                notes: character.notes
            };
            showCharacterForm.value = true;
        }

        async function saveCharacter() {
            if (!characterForm.value.name) {
                showAlert('提示', '请输入角色名称');
                return;
            }

            try {
                const charData = {
                    name: characterForm.value.name,
                    hp: characterForm.value.hp,
                    max_hp: characterForm.value.max_hp,
                    attack_bonus: characterForm.value.attack_bonus,
                    damage_dice: characterForm.value.damage_dice,
                    notes: characterForm.value.notes
                };

                if (editingCharacter.value) {
                    // 更新角色卡
                    await axios.put(
                        `${API_BASE}/api/characters/${editingCharacter.value.id}`,
                        charData,
                        { headers: authHeaders() }
                    );
                } else {
                    // 创建角色卡
                    await axios.post(
                        `${API_BASE}/api/rooms/${currentRoom.value.id}/characters`,
                        charData,
                        { headers: authHeaders() }
                    );
                }

                closeCharacterForm();
                fetchRoomCharacters(currentRoom.value.id);
            } catch (e) {
                showAlert('保存失败', e.response?.data?.detail || e.message);
            }
        }

        function closeCharacterForm() {
            showCharacterForm.value = false;
            editingCharacter.value = null;
            characterForm.value = {
                name: '',
                hp: 1,
                max_hp: 1,
                attack_bonus: 1,
                damage_dice: '1d6',
                notes: ''
            };
        }

        // 模态框状态
        const showModal = ref(false);
        const modalTitle = ref('');
        const modalBody = ref('');
        const modalType = ref('alert'); // alert, prompt, confirm
        const modalInputValue = ref('');
        const modalCallback = ref(null);
        const modalInputPlaceholder = ref('');

        // 检查登录状态
        if (token.value) {
            fetchCurrentUser();
        }

        // API 请求头
        const authHeaders = () => ({ Authorization: `Bearer ${token.value}` });

        // ============ 模态框相关 ============

        function showAlert(title, message, callback = null) {
            modalTitle.value = title;
            modalBody.value = message;
            modalType.value = 'alert';
            showModal.value = true;
            modalCallback.value = callback;
        }

        function showPrompt(title, message, placeholder = '', defaultValue = '') {
            return new Promise((resolve) => {
                modalTitle.value = title;
                modalBody.value = message;
                modalInputPlaceholder.value = placeholder;
                modalInputValue.value = defaultValue;
                modalType.value = 'prompt';
                showModal.value = true;
                modalCallback.value = (result) => {
                    resolve(result);
                };
            });
        }

        function showConfirm(title, message) {
            return new Promise((resolve) => {
                modalTitle.value = title;
                modalBody.value = message;
                modalType.value = 'confirm';
                showModal.value = true;
                modalCallback.value = (result) => {
                    resolve(result);
                };
            });
        }

        function handleModalConfirm() {
            if (modalType.value === 'prompt') {
                if (modalCallback.value) modalCallback.value(modalInputValue.value);
            } else if (modalCallback.value) {
                modalCallback.value(true);
            }
            showModal.value = false;
            modalCallback.value = null;
        }

        function handleModalCancel() {
            if (modalType.value === 'prompt') {
                if (modalCallback.value) modalCallback.value(null);
            } else if (modalCallback.value) {
                modalCallback.value(false);
            }
            showModal.value = false;
            modalCallback.value = null;
        }

        // ============ 认证相关 ============

        async function login() {
            try {
                const formData = new FormData();
                formData.append('username', loginForm.value.username);
                formData.append('password', loginForm.value.password);

                const resp = await axios.post(`${API_BASE}/api/auth/login`, formData);
                token.value = resp.data.access_token;
                localStorage.setItem('token', token.value);
                await fetchCurrentUser();
                currentView.value = 'dashboard';
                fetchModules();
            } catch (e) {
                showAlert('登录失败', e.response?.data?.detail || e.message);
            }
        }

        async function register() {
            try {
                await axios.post(`${API_BASE}/api/auth/register`, {
                    username: registerForm.value.username,
                    password: registerForm.value.password,
                    can_create_module: registerForm.value.can_create_module
                });
                showAlert('注册成功', '请登录', () => {
                    currentView.value = 'login';
                });
            } catch (e) {
                showAlert('注册失败', e.response?.data?.detail || e.message);
            }
        }

        async function fetchCurrentUser() {
            try {
                const resp = await axios.get(`${API_BASE}/api/auth/me`, { headers: authHeaders() });
                currentUser.value = resp.data;
            } catch (e) {
                logout();
            }
        }

        function logout() {
            token.value = null;
            localStorage.removeItem('token');
            currentUser.value = null;
            currentView.value = 'login';
        }

        // ============ 模组相关 ============

        async function fetchModules() {
            try {
                const resp = await axios.get(`${API_BASE}/api/modules`, { headers: authHeaders() });
                modules.value = resp.data;
            } catch (e) {
                console.error('获取模组失败', e);
            }
        }

        async function createModule() {
            const title = await showPrompt('创建模组', '请输入模组名称:', '模组名称');
            if (!title) return;

            const description = await showPrompt('创建模组', '请输入模组描述:', '模组描述');

            try {
                await axios.post(`${API_BASE}/api/modules`, { title, description }, { headers: authHeaders() });
                fetchModules();
            } catch (e) {
                showAlert('创建失败', e.response?.data?.detail || e.message);
            }
        }

        async function openModule(module) {
            currentModule.value = module;
            currentView.value = 'module-edit';
            fetchResources(module.id);
        }

        // ============ 资源相关 ============

        async function fetchResources(moduleId) {
            try {
                const resp = await axios.get(`${API_BASE}/api/modules/${moduleId}/resources`, { headers: authHeaders() });
                resources.value = resp.data;
            } catch (e) {
                console.error('获取资源失败', e);
            }
        }

        async function createResource() {
            if (!selectedFile.value && newResource.value.type === 'image') {
                showAlert('提示', '请选择图片文件');
                return;
            }

            try {
                if (newResource.value.type === 'text') {
                    const formData = new FormData();
                    formData.append('title', newResource.value.title);
                    formData.append('type', 'text');
                    formData.append('display_type', newResource.value.display_type);
                    formData.append('content', newResource.value.content);

                    await axios.post(`${API_BASE}/api/modules/${currentModule.value.id}/resources`, formData, {
                        headers: { ...authHeaders(), 'Content-Type': 'multipart/form-data' }
                    });
                } else {
                    const formData = new FormData();
                    formData.append('title', newResource.value.title || '未命名图片');
                    formData.append('type', 'image');
                    formData.append('file', selectedFile.value);

                    await axios.post(`${API_BASE}/api/modules/${currentModule.value.id}/resources`, formData, {
                        headers: authHeaders()
                    });
                }

                showResourceForm.value = false;
                newResource.value = { type: 'text', title: '', content: '', display_type: 'story' };
                selectedFile.value = null;
                fetchResources(currentModule.value.id);
            } catch (e) {
                showAlert('创建资源失败', e.response?.data?.detail || e.message);
            }
        }

        function handleFileSelect(e) {
            selectedFile.value = e.target.files[0];
        }

        async function toggleVisibility(resource) {
            try {
                await axios.post(`${API_BASE}/api/resources/${resource.id}/toggle-visible`,
                    { default_visible: !resource.default_visible },
                    { headers: { ...authHeaders(), 'Content-Type': 'application/json' } }
                );
                fetchResources(currentModule.value.id);
            } catch (e) {
                showAlert('操作失败', e.response?.data?.detail || e.message);
            }
        }

        async function deleteResource(resource) {
            const confirmed = await showConfirm('确认删除', `确定要删除资源 "${resource.title}" 吗？`);
            if (!confirmed) return;

            try {
                await axios.delete(`${API_BASE}/api/resources/${resource.id}`, { headers: authHeaders() });
                fetchResources(currentModule.value.id);
            } catch (e) {
                showAlert('删除失败', e.response?.data?.detail || e.message);
            }
        }

        // ============ 导航相关 ============

        async function goToDashboard() {
            currentView.value = 'dashboard';
            await fetchModules();
        }

        async function goToRoomList() {
            currentView.value = 'room-list';
            await fetchAllModules();
            await fetchAllRooms();
        }

        async function goToRoomManage() {
            currentView.value = 'room-manage';
            await fetchModules();
            await fetchGMRooms();
        }

        // ============ 房间相关 ============

        async function createRoom(module) {
            const name = await showPrompt('创建房间', '请输入房间名称:', '房间名称');
            if (!name) return;

            try {
                const resp = await axios.post(`${API_BASE}/api/modules/${module.id}/rooms`, { name }, { headers: authHeaders() });
                // 创建成功，进入游戏房间
                const newRoom = resp.data;
                currentRoom.value = newRoom;
                isGM.value = true;
                currentView.value = 'game';

                // 加载房间数据
                loadRoomData(newRoom.id);
                // 启动日志轮询
                startLogPolling(newRoom.id);
            } catch (e) {
                showAlert('创建失败', e.response?.data?.detail || e.message);
            }
        }

        async function fetchRooms(moduleId) {
            try {
                const resp = await axios.get(`${API_BASE}/api/modules/${moduleId}/rooms`, { headers: authHeaders() });
                rooms.value = resp.data;
                currentView.value = 'rooms';
            } catch (e) {
                console.error('获取房间失败', e);
            }
        }

        // 显示房间列表（玩家版）
        async function showRoomList() {
            currentView.value = 'room-list';
            await fetchAllModules();
            await fetchAllRooms();
        }

        // 获取所有模组（用于筛选）
        async function fetchAllModules() {
            try {
                const resp = await axios.get(`${API_BASE}/api/modules`, { headers: authHeaders() });
                allModules.value = resp.data;
            } catch (e) {
                console.error('获取模组失败', e);
            }
        }

        // 获取所有房间（玩家版）
        async function fetchAllRooms() {
            try {
                let url = `${API_BASE}/api/rooms`;
                if (filterModuleId.value) {
                    url += `?module_id=${filterModuleId.value}`;
                }
                const resp = await axios.get(url, { headers: authHeaders() });
                allRooms.value = resp.data;
            } catch (e) {
                console.error('获取房间列表失败', e);
            }
        }

        // 获取状态标签
        function getStatusLabel(status) {
            const labels = {
                'waiting': '等待中',
                'active': '进行中',
                'ended': '已结束'
            };
            return labels[status] || status;
        }

        // 获取GM房间管理列表
        async function fetchGMRooms() {
            try {
                const resp = await axios.get(`${API_BASE}/api/rooms/gm`, { headers: authHeaders() });
                gmRooms.value = resp.data;
            } catch (e) {
                console.error('获取GM房间失败', e);
            }
        }

        // 显示创建房间对话框
        function showCreateRoomDialog() {
            if (modules.value.length === 0) {
                showAlert('提示', '请先创建模组');
                return;
            }
            selectedModuleId.value = null;
            showModuleSelect.value = true;
        }

        // 确认创建房间
        async function confirmCreateRoom() {
            if (!selectedModuleId.value) {
                showAlert('提示', '请选择模组');
                return;
            }

            const name = await showPrompt('创建房间', '请输入房间名称:', '房间名称');
            if (!name) return;

            try {
                const resp = await axios.post(`${API_BASE}/api/modules/${selectedModuleId.value}/rooms`, { name }, { headers: authHeaders() });
                // 创建成功，进入游戏房间
                const newRoom = resp.data;
                currentRoom.value = newRoom;
                isGM.value = true;
                currentView.value = 'game';
                showModuleSelect.value = false;

                // 加载房间数据
                loadRoomData(newRoom.id);
                // 启动日志轮询
                startLogPolling(newRoom.id);

                // 刷新GM房间列表
                fetchGMRooms();
            } catch (e) {
                showAlert('创建失败', e.response?.data?.detail || e.message);
            }
        }

        // 编辑房间名称
        async function editRoomName(room) {
            const newName = await showPrompt('编辑房间', '请输入新的房间名称:', '房间名称', room.name);
            if (!newName || newName === room.name) return;

            try {
                await axios.put(`${API_BASE}/api/rooms/${room.id}`, { name: newName }, { headers: authHeaders() });
                fetchGMRooms();
            } catch (e) {
                showAlert('编辑失败', e.response?.data?.detail || e.message);
            }
        }

        // 开始游戏
        async function startGame(room) {
            const confirmed = await showConfirm('开始游戏', `确定要开始游戏 "${room.name}" 吗？`);
            if (!confirmed) return;

            try {
                await axios.put(`${API_BASE}/api/rooms/${room.id}`, { status: 'active' }, { headers: authHeaders() });
                fetchGMRooms();
            } catch (e) {
                showAlert('操作失败', e.response?.data?.detail || e.message);
            }
        }

        // 结束游戏
        async function endGame(room) {
            const confirmed = await showConfirm('结束游戏', `确定要结束游戏 "${room.name}" 吗？`);
            if (!confirmed) return;

            try {
                await axios.put(`${API_BASE}/api/rooms/${room.id}`, { status: 'ended' }, { headers: authHeaders() });
                fetchGMRooms();
            } catch (e) {
                showAlert('操作失败', e.response?.data?.detail || e.message);
            }
        }

        // 删除房间
        async function deleteRoom(room) {
            const confirmed = await showConfirm('确认删除', `确定要删除房间 "${room.name}" 吗？此操作不可恢复！`);
            if (!confirmed) return;

            try {
                await axios.delete(`${API_BASE}/api/rooms/${room.id}`, { headers: authHeaders() });
                fetchGMRooms();
            } catch (e) {
                showAlert('删除失败', e.response?.data?.detail || e.message);
            }
        }

        return {
            // 状态
            currentView,
            currentUser,
            API_BASE,
            loginForm,
            registerForm,
            modules,
            currentModule,
            resources,
            showResourceForm,
            newResource,
            rooms,

            // 游戏房间
            currentRoom,
            roomResources,
            roomCharacters,
            gameLogs,
            isGM,
            myCharacter,
            logContainer,

            // 掷骰子
            selectedDice,
            diceModifier,
            diceResult,

            // 角色卡
            showCharacterForm,
            editingCharacter,
            characterForm,
            attackResult,

            // 模态框
            showModal,
            modalTitle,
            modalBody,
            modalType,
            modalInputValue,
            modalInputPlaceholder,

            // 认证
            login,
            register,
            logout,

            // 模组
            createModule,
            openModule,
            createResource,
            handleFileSelect,
            toggleVisibility,
            deleteResource,

            // 导航
            goToDashboard,
            goToRoomList,
            goToRoomManage,

            // 房间
            createRoom,
            joinRoom,
            leaveRoom,
            allRooms,
            allModules,
            filterModuleId,
            gmRooms,
            showModuleSelect,
            selectedModuleId,
            showRoomList,
            fetchAllRooms,
            fetchGMRooms,
            getStatusLabel,
            showCreateRoomDialog,
            confirmCreateRoom,
            editRoomName,
            startGame,
            endGame,
            deleteRoom,

            // 游戏
            fetchRoomDetails,
            loadRoomData,
            rollDice,
            quickAttack,
            toggleResourceVisibility,
            handleImageError,
            getDisplayTypeLabel,
            formatTime,

            // 角色卡
            editCharacter,
            saveCharacter,
            closeCharacterForm,

            // 模态框
            handleModalConfirm,
            handleModalCancel
        };
    }
}).mount('#app');