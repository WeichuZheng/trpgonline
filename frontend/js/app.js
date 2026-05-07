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

        // 检查登录状态
        if (token.value) {
            fetchCurrentUser();
        }

        // API 请求头
        const authHeaders = () => ({ Authorization: `Bearer ${token.value}` });

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
                alert('登录失败: ' + (e.response?.data?.detail || e.message));
            }
        }

        async function register() {
            try {
                await axios.post(`${API_BASE}/api/auth/register`, {
                    username: registerForm.value.username,
                    password: registerForm.value.password,
                    can_create_module: registerForm.value.can_create_module
                });
                alert('注册成功，请登录');
                currentView.value = 'login';
            } catch (e) {
                alert('注册失败: ' + (e.response?.data?.detail || e.message));
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
            const title = prompt('请输入模组名称:');
            if (!title) return;
            const description = prompt('请输入模组描述:');

            try {
                await axios.post(`${API_BASE}/api/modules`, { title, description }, { headers: authHeaders() });
                fetchModules();
            } catch (e) {
                alert('创建失败: ' + (e.response?.data?.detail || e.message));
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
                alert('请选择图片文件');
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
                alert('创建资源失败: ' + (e.response?.data?.detail || e.message));
            }
        }

        function handleFileSelect(e) {
            selectedFile.value = e.target.files[0];
        }

        async function toggleVisibility(resource) {
            try {
                await axios.post(`${API_BASE}/api/resources/${resource.id}/toggle-visible`,
                    { is_visible: !resource.is_visible },
                    { headers: { ...authHeaders(), 'Content-Type': 'application/json' } }
                );
                fetchResources(currentModule.value.id);
            } catch (e) {
                alert('操作失败: ' + (e.response?.data?.detail || e.message));
            }
        }

        async function deleteResource(resource) {
            if (!confirm('确定要删除这个资源吗？')) return;

            try {
                await axios.delete(`${API_BASE}/api/resources/${resource.id}`, { headers: authHeaders() });
                fetchResources(currentModule.value.id);
            } catch (e) {
                alert('删除失败: ' + (e.response?.data?.detail || e.message));
            }
        }

        // ============ 房间相关 ============

        async function createRoom(module) {
            const name = prompt('请输入房间名称:');
            if (!name) return;

            try {
                await axios.post(`${API_BASE}/api/modules/${module.id}/rooms`, { name }, { headers: authHeaders() });
                alert('房间创建成功！');
                fetchRooms(module.id);
            } catch (e) {
                alert('创建失败: ' + (e.response?.data?.detail || e.message));
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

        return {
            currentView,
            currentUser,
            loginForm,
            registerForm,
            modules,
            currentModule,
            resources,
            showResourceForm,
            newResource,
            rooms,
            login,
            register,
            logout,
            createModule,
            openModule,
            createResource,
            handleFileSelect,
            toggleVisibility,
            deleteResource,
            createRoom
        };
    }
}).mount('#app');