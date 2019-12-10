<template>
  <div class="hello">
    <h3>{{ msg }}</h3>
    <p>
      For a guide and recipes on how to configure / customize this project,<br>
      check out the
      <a href="https://cli.vuejs.org" target="_blank" rel="noopener">vue-cli documentation</a>.
    </p>
    <h3>Choose product:</h3>
    <br>
     <div v-for="name in rootList" :key='name' style="margin-top:5px;">
        <input type="radio" v-bind:value="name" v-model="selectedName" />
        <label> {{name}}</label><br />
      </div>
      <hr>
      <div>
        <p><input name="subDir" type="radio" value="\" checked> \</p>
        <p><input name="subDir" type="radio" value="_Main"> _Main</p>
        <p><input name="subDir" type="radio" value="_Internal" > _Internal</p>
        <p><input name="subDir" type="radio" value="_External" > _External</p>
      </div>

  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  props: {
    msg: String,
    rootList: Array,
    name: String
    
  },
  data: function() {
    return {
        selectedName: ""
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
