<template>
  <div class="similars">
    <h1>類似記事</h1>
    <b-table id="similars-table" :items="sharedSimilars" :fields="ibFields">
      <template slot="ib_title" slot-scope="data">
        <a :href="'https://ja.wikipedia.org/wiki/Template:' + data.value" target="_blank">{{data.value}}</a>
      </template>
      <template slot="similars" slot-scope="data">
        {{data.value.length}}ページ
      </template>
      <template slot="show_similars" slot-scope="row">
        <b-button size="sm" @click.stop="row.toggleDetails" class="mr-2">
          類似記事を{{ row.detailsShowing ? '隠す':'表示'}}
        </b-button>
        <b-button size="sm" @click="regenerate(row.item.ib_title)" class="mr-2">
          記事テンプレート再生成
        </b-button>
      </template>
      <template slot="row-details" slot-scope="row">
        <b-table id="similars-table" :items="row.item.similars" :fields="similarsFields" :outlined="outlined">
          <template slot="title" slot-scope="data">
            <a :href="'https://ja.wikipedia.org/wiki/' + data.value" target="_blank">{{data.value}}</a>
          </template>
          <template slot="sections" slot-scope="data">
            {{data.value.join(', ')}}
          </template>
        </b-table>
      </template>
      <template slot="table-caption">
        {{ sharedSimilars.length }} 種類の Infobox が存在しています．
      </template>
    </b-table>
  </div>
</template>

<script>
import store from '@/store'
export default {
  name: 'SimilarsList',
  data () {
    return {
      sharedSimilars: store.state.similars,
      outlined: true,
      ibFields: [
        {key: 'ib_title', label: 'Infobox'},
        {key: 'similars', label: '類似記事数'},
        {key: 'show_similars', label: ''}
      ],
      similarsFields: [
        {key: 'title', label: '記事名'},
        {key: 'sections', label: '章構成'}
      ]
    }
  },
  methods: {
    regenerate (infobox) {
      this.$emit('regenerate', infobox)
      this.$router.push({name: 'Template'})
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .similars {
    height: 100%;
  }
  #similars-table {
    font-size: 15px;
  }
</style>
