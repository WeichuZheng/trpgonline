import { Extension } from '@tiptap/core'

export const VISIBILITY_VISIBLE = 'visible'
export const VISIBILITY_GM_ONLY = 'gm-only'
export const VISIBILITY_HIDDEN = 'hidden'

export const VisibilityExtension = Extension.create({
  name: 'visibility',

  addOptions() {
    return { types: ['heading', 'paragraph', 'bulletList', 'orderedList', 'blockquote', 'image', 'horizontalRule'] }
  },

  addGlobalAttributes() {
    return [
      {
        types: this.options.types,
        attributes: {
          visibility: {
            default: VISIBILITY_VISIBLE,
            parseHTML: element => element.dataset.visibility || VISIBILITY_VISIBLE,
            renderHTML: attributes => {
              if (!attributes.visibility || attributes.visibility === VISIBILITY_VISIBLE) return {}
              return { 'data-visibility': attributes.visibility }
            },
          },
        },
      },
    ]
  },

  addCommands() {
    return {
      setVisibility: visibility => ({ commands, state }) => {
        const { from, to } = state.selection
        let affected = false
        state.doc.nodesBetween(from, to, node => {
          if (this.options.types.includes(node.type.name)) {
            commands.updateAttributes(node.type.name, { visibility })
            affected = true
          }
        })
        return affected
      },
    }
  },
})
