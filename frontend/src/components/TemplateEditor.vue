<template>
  <div class="template">
    <h1>記事テンプレート</h1>
    <p><b>記事名:</b> {{ sharedTemplate.title }}</p>
    <p><b>Infobox:</b> <a :href="url" target="_blank">{{ sharedTemplate.infobox }}</a></p>
    <p><b>章構成:</b> {{ sharedTemplate.sections }}</p>
    <p><b>wikiテンプレート:</b></p>
    <textarea v-model="sharedTemplate.wiki" name="wiki" cols="60"></textarea>
  </div>
</template>

<script>
import store from '@/store'
export default {
  name: 'TemplateEditor',
  data () {
    return {
      sharedTemplate: store.state.template
    }
  },
  computed: {
    url: function () {
      return 'https://ja.wikipedia.org/wiki/Template:' + this.sharedTemplate.infobox
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .template {
    height: 100%;
  }
  textarea {
    width: 100%;
    height: 65%;
  }
</style>
