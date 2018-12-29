<template>
  <b-navbar toggleable="md" type="dark" variant="info">
      <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>
      <router-link :to="{name:'Template'}">
        <b-navbar-brand tag="h1">Wikiplate</b-navbar-brand>
      </router-link>
  <b-collapse is-nav id="nav_collapse">
    <!-- Right aligned nav items -->
    <b-navbar-nav class="ml-auto">
      <b-nav-form class="form">
        <b-form-input size="sm" class="col-sm-8 mr-sm-2" type="text" v-model="privateState.keywords" placeholder="キーワード(城:史跡)"/>
        <b-button size="sm" class="my-2 my-sm-0" @click="create">作成</b-button>
      </b-nav-form>
    </b-navbar-nav>
  </b-collapse>
  </b-navbar>
</template>

<script>
export default {
  data () {
    return {
      privateState: {
        keywords: ''
      }
    }
  },
  methods: {
    create () {
      this.$emit('create', this.privateState.keywords)
    }
  }
}
</script>

<style>
  .form {
    height: 100%;
  }
</style>
