<template>
  <div id="app">
    <!-- <img alt="Vue logo" src="./assets/logo.png"> -->
    <!-- <HelloWorld msg="Welcome to Your Vue.js App"/> -->

    <h2>{{ message }}</h2>
    <hr />
    <h3>Setup:</h3>
    <input v-model="setupPath" placeholder="Input setup path" size="150" />
    <br />
    <button @click="req" style="margin-top: 20px;">
      Request VM
    </button>
    <br />

    <h3>Choose Virtual Machine:</h3>
    <table>
      <tr>
        <th style="text-align:center;">Free</th>
        <th style="text-align:center;">Busy</th>
      </tr>
      
        <tr>
          <td>
            <div v-for="(name, key) in cfg" @change="clearSn" :key='key'>
              <div v-if="cfg[key].status=='free'">
                <input type="radio" v-bind:value="key" v-model="selectedVm" />
                <label>{{key}}</label><br />
              </div>
            </div>
          </td>
          <td vlign="top">
            <div v-for="(name, key) in cfg" @change="clearSn" :key='key'>
              <ul>
                <li style="list-style-type:none;" v-if="cfg[key].status=='busy'">{{key}}</li>
              </ul>
            </div>
          </td>


        </tr>
    </table>
      
    
    <hr />
    <!-- <span v-if="selectedVm!==null">Выбрано: {{selectedVm}}</span> -->
    <br />
    <div v-if="selectedVm!==null">
      <h3>Choose Snapshot:</h3>
      <div v-for="sn in cfg[selectedVm].sn" :key='sn'>
        <input type="radio" v-bind:value="sn" v-model="selectedSn" />
        <label>{{sn}}</label><br />
      </div>
      <hr />
      <table border="1" cellpadding="7" bordercolor="silver">
        <tr>
          <td>Setup path:</td>
          <td>{{setupPath}}</td>
        </tr>
        <tr>
          <td>Virtual Machine:</td>
          <td>{{selectedVm}}</td>
        </tr>
        <tr>
          <td>Snapshot:</td>
          <td>{{selectedSn}}</td>
        </tr>
      </table>
    </div>
    <button :disabled="selectedSn==null" @click="singleTask" style="margin-top: 20px;">
      Start single task
    </button>
    <p>Task status: {{messageOk}}</p>
    <!-- <p>{{cfg}}</p> -->


  </div>
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'

export default {
  name: 'app',
  // components: {
  //   HelloWorld
  // },
        data: function() {return {
        message: "Hello Victor!",
        cfg: {},
        selectedVm: null,
        selectedSn: null,
        setupPath: null,
        singleCfg: {},
        messageOk: 'Not started'
      }},

      methods: {
        req: function () {
          this.cfg = {};
          this.selectedVm = null;
          const url = "http://127.0.0.1:5000/api/cfg";
          fetch(url, {
            method: "GET",
            headers: {
              "Content-Type": "application/json;charset=utf-8",
              "Access-Control-Allow-Origin": "*"
            }
          })
            .then(response => response.json()) // преобразуем ответ в json
            .then(data => {
              this.cfg = data;
              // this.console.log('bbbb')
            })
            .catch(error => this.console.error(error));
        },
        clearSn: function () {
          this.selectedSn = null;
          this.messageOk ='Not started';
        },
        singleTask: function () {
          this.singleCfg.path = this.setupPath;
          this.singleCfg.vm = this.selectedVm;
          this.singleCfg.snapshot = this.selectedSn;
          this.messageOk = 'Running. Wait for finish';
          this.console.log(this.singleCfg);

          const url = "http://127.0.0.1:5000/api/single";
          fetch(url, {
            method: "POST",
            headers: {
              "Content-Type": "application/json;charset=utf-8"
            },
            body: JSON.stringify(this.singleCfg)
          })
            .then(response => response.json()) // преобразуем ответ в json
            .then(data => {
              this.console.log(data);
              this.messageOk ='Finished';
            })
            .catch(error => this.console.error(error));
        }
      }
    };

</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;
  color: #2c3e50;
  margin-top: 30px;
}
</style>
