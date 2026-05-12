import Image from '@tiptap/extension-image'

export const CustomImage = Image.extend({
  addAttributes() {
    return {
      ...this.parent?.(),
      width: {
        default: null,
        parseHTML: element => element.getAttribute('width') || element.style.width || null,
        renderHTML: attributes => {
          if (!attributes.width) return {}
          return { width: attributes.width }
        },
      },
    }
  },

  renderHTML({ HTMLAttributes }) {
    // Extract text-align from the merged style attribute
    // (set by TextAlign extension — text-align on <img> is ineffective)
    let align = null
    if (HTMLAttributes.style) {
      const match = HTMLAttributes.style.match(/text-align:\s*(left|center|right|justify)/)
      if (match) {
        align = match[1]
        // Remove text-align from the <img> style
        HTMLAttributes.style = HTMLAttributes.style.replace(/text-align:\s*(left|center|right|justify);?\s*/, '').trim()
        if (!HTMLAttributes.style) delete HTMLAttributes.style
      }
    }

    if (align === 'center') {
      return ['div', { style: 'text-align: center' }, ['img', HTMLAttributes]]
    }
    if (align === 'right') {
      return ['div', { style: 'text-align: right' }, ['img', HTMLAttributes]]
    }
    return ['img', HTMLAttributes]
  },
})
