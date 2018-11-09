<template>
  <div class="similars">
    <h1>類似記事</h1>
    <b-table id="similars-table" :items="sharedSimilars" :fields="fields" :per-page="perPage" :current-page="currentPage">
      <template slot="title" slot-scope="data">
        <a :href="'https://ja.wikipedia.org/wiki/' + data.value" target="_blank">{{data.value}}</a>
      </template>
      <template slot="sections" slot-scope="data">
        {{data.value.join(', ')}}
      </template>
      <template slot="table-caption">
        {{ sharedSimilars.length }} 件の類似記事が抽出されました．
      </template>
    </b-table>
    <b-pagination class="pagination" align="center" size="sm" :total-rows="sharedSimilars.length" :per-page="perPage" v-model="currentPage">
    </b-pagination>
  </div>
</template>

<script>
import store from '@/store'
export default {
  name: 'SimilarsList',
  data () {
    return {
      sharedSimilars: store.state.similars,
      currentPage: 1,
      perPage: 6,
      fields: [
        {key: 'title', label: '記事名', sortable: true},
        {key: 'infobox', label: 'Infobox', sortable: true},
        {key: 'sections', label: '章構成', sortable: true}
      ]
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
