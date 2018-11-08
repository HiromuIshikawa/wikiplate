<template>
  <div id="app">
    <nav-bar class="navbar" @create="create"/>
    <b-container class="main-container">
      <b-row class="main-row">
        <b-col class="sidebar-col" cols="12" sm="2"><side-bar/></b-col>
        <b-col class="main-content-col" cols="12" sm="10"><router-view/></b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import store from '@/store'
import SideBar from '@/components/SideBar'
import NavBar from '@/components/NavBar'
export default {
  name: 'App',
  components: {
    SideBar,
    NavBar
  },
  data () {
    return {
      sharedState: store.state
    }
  },
  methods: {
    create (title, keywords) {
      store.actions.getTemplate(title, keywords)
    }
  }
}
</script>

<style>
  html {
    height: 100%;
  }
  body {
    background-color: whitesmoke;
    font-size: 18px;
    height: 100%;
  }
  #app {
    height: 100%;
  }
  .main-container {
    background-color: white;
    height: 90%;
  }
  .main-row {
    height: 100%;
  }
  .sidebar-col {
    padding: 0px;
    height: 100%;
    background-color: gray;
  }
  .main-content-col {
    height: 100%;
  }
  .main-content-col h1 {
    color: #666;
    font-size: 25px;
    padding-bottom: 0.3em;
    border-bottom: solid 2px #999;
  }
</style>
