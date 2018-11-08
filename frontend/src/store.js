// import axios from 'axios'
// const apiEndpoint = 'http://localhost:5000/api'

const state = {
  template: {
    title: '岡山大学',
    infobox: '大学',
    sections: ['概要', '沿革', '基礎データ', '教育および研究', '学生生活', '大学関係者と組織', '関連項目', '外部リンク'],
    wiki: '{{ 大学\n|国  =\n|大学名  =\n|ふりがな  =\n|英称  =\n|公用語表記  =\n|大学の略称  =\n|画像  =\n|pxl  =\n|画像説明  =\n|大学設置年  =\n|創立年  =\n|学校種別  =\n|設置者  =\n|本部所在地  =\n|緯度度 = |緯度分 = |緯度秒  =\n|経度度 = |経度分 = |経度秒  =\n|キャンパス  =\n|学部  =\n|研究科  =\n|ウェブサイト  =\n|緯度度 = |緯度分 = |緯度秒 = |N(北緯)及びS(南緯)  =\n|経度度 = |経度分 = |経度秒 = |E(東経)及びW(西経)  =\n|地図国コード  =\n}}\n\n== 概要 ==\n\n== 沿革 ==\n\n== 基礎データ ==\n\n== 教育および研究 ==\n\n== 学生生活 ==\n\n== 大学関係者と組織 ==\n\n== 関連項目 ==\n\n== 外部リンク ==\n'
  },
  similars: [
    {title: '香川大学'},
    {title: '岡山理科大学'},
    {title: '広島大学'}
  ]
}

const actions = {
  getTemplate (title, keywords) {
    // TODO: Get Tempalate from Flask server
    state.template.title = title
  }
}

export default {
  state,
  actions
}