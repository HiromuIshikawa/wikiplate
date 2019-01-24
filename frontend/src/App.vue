<template>
  <div id="app">
    <nav-bar class="navbar" @create="create"/>
    <b-container class="main-container">
      <b-row class="main-row">
        <b-col class="sidebar-col" cols="12" sm="2"><side-bar/></b-col>
        <b-col v-if="sharedState.loading" class="loading-col" cols="12" sm = "10">
          <sync-loader class="loader" :loading="sharedState.loading" :color="color" :size="size" :margin="margin"></sync-loader>
          <p class="loader-text">記事テンプレートを生成しています</p>
          <p class="rate">{{ rate }} %</p>
          <b-progress class="mb-2 treat-bar" :value="sharedState.treatPairs" :max="sharedState.allPairs" variant="info" animated></b-progress>
        </b-col>
        <b-col v-else class="main-content-col" cols="12" sm="10"><router-view @regenerate="regenerate" /></b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import store from '@/store'
import SideBar from '@/components/SideBar'
import NavBar from '@/components/NavBar'
import SyncLoader from 'vue-spinner/src/SyncLoader'
import 'normalize.css'

export default {
  name: 'App',
  components: {
    SideBar,
    NavBar,
    SyncLoader
  },
  data () {
    return {
      sharedState: store.state,
      color: '#5bc0de',
      size: '20px',
      margin: '10px',
      radius: '2px'
    }
  },
  computed: {
    rate: function () {
      return Math.round(this.sharedState.treatPairs / this.sharedState.allPairs * 100)
    }
  },
  methods: {
    create (keywords) {
      store.actions.getTemplate(keywords)
    },
    regenerate (infobox) {
      store.actions.regenerateTemplate(infobox)
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
    background-color: whitesmoke;
  }
  .main-container {
    background-color: white;
    height: 90%;
  }
  .main-row {
    height: 100%;
  }
  .navbar {
    box-shadow: 0px 0px 5px #444;
    z-index: 3;
  }
  div.sidebar-col {
    padding: 0;
    height: 100%;
    background-color: gray;
    box-shadow: 0px 0px 5px #444;
    z-index: 2;
  }
  div.main-content-col {
    padding-top: 5px;
    height: 100%;
    overflow: auto;
    box-shadow: 0px 0px 5px #444;
    z-index: 1;
    color: #555;
    font-size: 17px;
  }
  div.loading-col {
    height: 100%;
    box-shadow: 0px 0px 5px #444;
    z-index: 1;
  }
  .main-content-col h1 {
    color: #666;
    font-size: 25px;
    padding-bottom: 0.3em;
    border-bottom: solid 2px #999;
  }
  .loader {
    position: absolute;
    top: 63%;
    left: 50%;
    -webkit-transform: translateY(-50%) translateX(-50%);
    transform: translateY(-50%) translateX(-50%);
  }
  .loader-text {
    text-align: center;
    font-size: 25px;
    color: #5bc0de;
    position: absolute;
    top: 40%;
    left: 50%;
    -webkit-transform: translateY(-50%) translateX(-50%);
    transform: translateY(-50%) translateX(-50%);
  }
  .rate {
    text-align: center;
    font-size: 18px;
    color: #5bc0de;
    position: absolute;
    top: 54%;
    left: 50%;
    -webkit-transform: translateY(-50%) translateX(-50%);
    transform: translateY(-50%) translateX(-50%);
  }
  .treat-bar {
    position: absolute;
    font-size: 20px;
    top: 50%;
    left: 50%;
    width: 80%;
    height: 3%;
    -webkit-transform: translateY(-50%) translateX(-50%);
    transform: translateY(-50%) translateX(-50%);
  }
</style>
