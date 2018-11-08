<template>
  <div class="sidebar">
    <router-link class= "sidebar-item" tag="div" :to="{ name: 'Template'}" exact>記事テンプレート</router-link>
    <router-link class= "sidebar-item" tag="div" :to="{ name: 'Similars'}">類似記事</router-link>
  </div>
</template>

<script>
export default {
  name: 'SideBar'
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .sidebar-item {
    background-color: gray;
    padding-left: 12%;
    padding-top: 0.5%;
    font-size: 20px;
    color: white;
    cursor: pointer;
  }

  .sidebar-item:hover {
    background-color: rgb(91, 91, 91);
  }

  .router-link-active {
    background-color: rgb(91,91,91);
  }
</style>
