import { Node } from '@tiptap/core'

export const ColumnLayout = Node.create({
  name: 'columnLayout',
  group: 'block',
  content: 'column column',
  defining: true,
  isolating: true,

  addAttributes() {
    return {
      gap: { default: '16px' }
    }
  },

  parseHTML() {
    return [{ tag: 'div[class~="column-layout"]' }]
  },

  renderHTML({ HTMLAttributes }) {
    return ['div', { class: 'column-layout', style: `display:flex; gap:16px` }, 0]
  },

  addCommands() {
    return {
      toggleColumnLayout: () => ({ editor, chain, commands }) => {
        if (editor.isActive('columnLayout')) {
          // Unwrap columns back to plain blocks
          const { state } = editor
          const { from, to } = state.selection
          const resolved = state.doc.resolve(from)
          const columnLayout = resolved.node(-1)
          if (columnLayout && columnLayout.type.name === 'columnLayout') {
            const start = resolved.start(-1)
            chain()
              .setTextSelection({ from: start, to: start + columnLayout.nodeSize - 2 })
              .liftListItem('listItem')
              .run()
            // Manually replace with inner content
            const children = []
            columnLayout.forEach((col, offset) => {
              col.forEach((child, childOffset) => {
                children.push(child)
              })
            })
            if (children.length > 0) {
              const newContent = state.schema.node('doc', null, children)
              const tr = state.tr.replaceWith(
                start, start + columnLayout.nodeSize,
                children
              )
              editor.view.dispatch(tr)
            }
          }
          return true
        }

        // Select current paragraph and next to wrap in columns
        const { from, to } = state.selection
        const paraNode = state.doc.resolve(from).node()
        const paraEnd = state.doc.resolve(to)

        // Find two block nodes to wrap
        const blocks = []
        state.doc.nodesBetween(from, Math.min(to + 1000, state.doc.content.size), (node, pos) => {
          if (node.isBlock && !node.type.name.startsWith('column')) {
            blocks.push({ node, pos })
            return false
          }
        })

        if (blocks.length < 2) {
          // Not enough blocks — create two empty columns
          return commands.insertContent({
            type: 'columnLayout',
            content: [
              { type: 'column', content: [{ type: 'paragraph' }] },
              { type: 'column', content: [{ type: 'paragraph' }] }
            ]
          })
        }

        const first = blocks[0]
        const second = blocks[1]
        const wrapFrom = first.pos
        const wrapTo = second.pos + second.node.nodeSize

        return commands.insertContentAt({ from: wrapTo, to: wrapTo }, {
          type: 'columnLayout',
          content: [
            { type: 'column', content: [first.node.toJSON()] },
            { type: 'column', content: [second.node.toJSON()] }
          ]
        }).then(() => {
          // Delete originals
          const tr = state.tr.delete(wrapFrom, wrapTo)
          editor.view.dispatch(tr)
          return true
        })
      }
    }
  },

  addKeyboardShortcuts() {
    return {
      'Backspace': () => {
        const { editor } = this
        const { empty, $anchor } = editor.state.selection
        if (!empty) return false
        // If cursor is at the very start of a column and it's the only content, unwrap
        const parent = $anchor.node(-2)
        if (parent && parent.type.name === 'columnLayout') {
          return editor.commands.toggleColumnLayout()
        }
        return false
      }
    }
  }
})

export const Column = Node.create({
  name: 'column',
  group: 'block',
  content: 'block+',
  defining: true,
  isolating: true,

  parseHTML() {
    return [{ tag: 'div[class~="column"]' }]
  },

  renderHTML({ HTMLAttributes }) {
    return ['div', { class: 'column', style: 'flex:1; min-width:0' }, 0]
  }
})
