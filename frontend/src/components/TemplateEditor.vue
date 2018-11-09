<template>
  <div class="template">
    <h1>記事テンプレート</h1>
    <b-row class="template-row">
      <b-col class="template-info" cols="12" sm="4">
        <p><b>記事名:</b> {{ sharedTemplate.title }}</p>
        <p><b>Infobox:</b> <a :href="url" target="_blank">{{ sharedTemplate.infobox.title }}</a></p>
        <p><b>章構成:</b></p>
        <div class="section-table">
          <div v-for="(section, index) in sharedTemplate.sections" :key="section">{{index+1}}. {{section}}</div>
        </div>
      </b-col>
      <b-col class="wiki-template" cols="12" sm="8">
        <p><b>wikiテンプレート:</b></p>
        <textarea v-model="sharedTemplate.wiki" name="wiki"></textarea>
      </b-col>
    </b-row>
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
      return this.sharedTemplate.infobox.url
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .template, .template-info, .wiki-template{
    height: 100%;
  }
  .template-row {
    height: 90%;
  }
  .section-table {
    margin-right: 0;
    padding: 0.5em 1em;
    border: solid 2px #888;
    border-radius: 10px;
  }
  textarea {
    width: 100%;
    height: 90%;
    border: solid 2px #888;
  }
</style>
