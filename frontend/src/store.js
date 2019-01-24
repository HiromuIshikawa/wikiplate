import axios from 'axios'
const apiEndpoint = 'https://wikiplate.herokuapp.com/api'
// const apiEndpoint = 'http://localhost:5000/api'

const state = {
  template: {
    infobox: {
      title: '',
      arg: [],
      url: ''
    },
    sections: [],
    wiki: ''
  },
  similars: [],
  loading: false,
  generating: false,
  allPairs: 1,
  treatPairs: 0,
  message: ''
}

const actions = {
  async getTemplate (keywords) {
    state.allPairs = 1
    state.treatPairs = 0
    state.loading = true
    const resPairs = await axios.get(apiEndpoint + '/pairs', {
      params: {
        keywords: keywords
      }
    }).catch(() => { console.log('pairs error') })
    if (resPairs.data.result === 'Success') {
      state.allPairs = resPairs.data.pairs + 1
      state.treatPairs = 1
      state.generating = true
    }
    while (state.generating) {
      const resTemplate = await axios.get(apiEndpoint + '/template').catch(() => { console.log('template error') })
      if (resTemplate.data.result === 'Success') {
        state.message = ''
        const resSimilars = await axios.get(apiEndpoint + '/similars').catch(() => { console.log('similars error') })
        const template = resTemplate.data
        const similars = resSimilars.data.similars
        for (let i = 0, len = similars.length; i < len; ++i) {
          if (similars[i].ib_title === template.infobox.title) {
            similars[i]._rowVariant = 'success'
          } else {
            similars[i]._rowVariant = ''
          }
        }
        state.template = Object.assign({}, template)
        state.similars = Object.assign([], similars)
        state.generating = false
        state.treatPairs = state.allPairs
      } else if (resTemplate.data.result === 'Generating now') {
        state.treatPairs = resTemplate.data.treat + 1
      } else {
        state.message = '類似記事が抽出できませんでした．'
        state.template = {
          infobox: {
            title: '',
            arg: [],
            url: ''
          },
          sections: [],
          wiki: ''
        }
        state.similars = []
        state.generating = false
      }
    }
    setTimeout(() => {
      state.loading = false
    }, 500)
  },
  async regenerateTemplate (infobox) {
    state.treatPairs = 0
    state.loading = true
    const resTemplate = await axios.get(apiEndpoint + '/regenerate', {
      params: {
        infobox: infobox
      }
    }).catch(() => { console.log('template error') })
    if (resTemplate.data.result === 'Success') {
      state.message = ''
      const template = resTemplate.data
      for (var i = 0, len = state.similars.length; i < len; ++i) {
        if (state.similars[i].ib_title === template.infobox.title) {
          state.similars[i]._rowVariant = 'success'
        } else {
          state.similars[i]._rowVariant = ''
        }
      }
      state.template = Object.assign({}, template)
    } else {
      state.message = '記事テンプレート生成に失敗しました．'
      state.template = {
        infobox: {
          title: '',
          arg: [],
          url: ''
        },
        sections: [],
        wiki: ''
      }
    }
    state.treatPairs = state.allPairs
    setTimeout(() => {
      state.loading = false
    }, 500)
  }
}

export default {
  state,
  actions
}
