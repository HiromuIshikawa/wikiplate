<template>
  <div class="similars">
    <h1>類似記事</h1>
    <div v-for="similar in sharedSimilars" :key="similar.title"><a :href="'https://ja.wikipedia.org/wiki/' + similar.title" target="_blank">{{similar.title}}</a></div>
  </div>
</template>

<script>
import store from '@/store'
export default {
  name: 'SimilarsList',
  data () {
    return {
      sharedSimilars: store.state.similars
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
