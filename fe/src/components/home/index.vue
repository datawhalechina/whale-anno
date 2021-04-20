<template>
  <div class="layout">
    <h1 class="out-title"><span class="home" @click="goHome">whaleAnno</span></h1>
    <div class="container">
      <div v-if="page==='list'" class="project-box">
        <div class="project-box-titile">
          <h3 class="inner-title">我的项目</h3>
          <div class="btn-area">
            <button class="button" @click="toEdit()">新建项目</button>
          </div>
        </div>
        <div class="list-box">
          <div v-if="projects.length === 0" class="project" style="border:none;color:#ccc;">暂无</div>
          <div class="project" v-for="project in projects" :key="project.projectName">
            <p class="name">{{project.projectName}}</p>
            <p class="type">{{project.projectType}}</p>
            <div class="btn-area">
              <button class="button" @click="toNerAnno(project)">开始标注</button>
              <button class="button" @click="toEdit(project)">配置</button>
            </div>
          </div>
        </div>
      </div>
      <div v-if="page==='edit' || page==='create'" class="edit-box">
        <p>名称：<input class="name-input" type="text" name="name" @change="setName" :value="name" :disabled="page==='edit'"/></p>
        <p>类型：
          <select class="type-input" name="type" @change="setType" :value="type">
            <option value ="命名实体识别">命名实体识别</option>
          </select>
        </p>
        <p class="edit-box-btn-area">
          <button class="button" @click="submit">提交</button>
          <button class="button" @click="toList">取消</button>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
function get (url, cb) {
  query('GET', url, '', cb)
}
function post (url, data, cb) {
  query('POST', url, data, cb)
}
function query (method, url, data = '', cb) {
  var xhr = new XMLHttpRequest()
  xhr.open(method, url)
  xhr.setRequestHeader('content-type', 'application/json')
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
      const result = JSON.parse(xhr.responseText)
      if (result.errCode !== 0) {
        alert(result.errMsg)
      } else {
        cb && cb(result.info)
      }
    }
  }
  xhr.send(JSON.stringify(data))
}

export default {
  name: 'home',
  data () {
    return {
      projects: [],
      name: '',
      type: '',
      page: 'list'
    }
  },
  computed: {
  },
  watch: {
    name: console.log
  },
  methods: {
    goHome () {
      this.page = 'list'
    },
    setName (ev) {
      this.name = ev.target.value
    },
    setType (ev) {
      this.type = ev.target.value
    },
    submit () {
      const that = this
      post('/v1/project/create', {
        projectName: that.name,
        projectType: that.type,
        entityTypes: ''
      }, function () {
        that.type = ''
        that.name = ''
        get('/v1/index', function (info) {
          that.$set(that, 'projects', info)
          that.name = ''
          that.type = ''
          that.page = 'list'
        })
      })
    },
    toNerAnno (project) {
      const { projectName, projectType, entityTypes } = project
      this.$router.push({path: '/NER', query: { projectName, projectType, entityTypes }})
    },
    toEdit (project = {}) {
      console.log('project', project)
      this.name = project.projectName || ''
      this.type = project.projectType || ''
      this.page = project.projectName ? 'edit' : 'create'
      console.log(this.name, 'this.name')
    },
    toList () {
      this.page = 'list'
    }
  },
  mounted () {
    const that = this
    // 加载项目列表
    get('/v1/index', function (info) {
      that.$set(that, 'projects', info)
    })
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.out-title {
  display: inline-block;
  background: #1161ca;
  color: white;
  margin: 0;
  width: 100%;
  height: 92px;
  line-height: 92px;
  border-bottom: 2px solid #ccc;
  box-sizing: border-box;
  vertical-align: middle;
}
.home {
  font-size: 28px;
  cursor: pointer;
}
.layout {
  display: flex;
  flex-direction: column;
}
.container {
  display: flex;
  flex: 1 1;
  flex-direction: row;
  /* height: calc(100% - 92px); */
}
.button {
  color: #fff;
  background-color: #1161ca;
  border-radius: 4px;
  border: 1px solid #ccc;
  padding: 5px 10px;
}
.project-box-titile {
  margin: auto;
  width: 500px;
  max-width: 100%;
  position: relative;
}
.project-box-titile .inner-title {
  margin: 0;
  line-height: 60px;
  height: 60px;
  text-align: left;
}
.project-box {
  width: 100%;
}
.list-box {
  margin: auto;
  width: 500px;
  max-width: 100%;
}
.project {
  position: relative;
  display: flex;
  box-sizing: border-box;
  margin-top: 10px;
  padding: 5px 10px;
  flex-direction: column;
  width: 100%;
  height: 60px;
  text-align: left;
  border: 1px solid #ccc;
}
.project .name,
.project .type {
  margin: 0;
}
.edit-box {
  width: 260px;
  margin: auto;
  margin-top: 0;
  text-align: left;
  padding: 5px 10px;
}
.edit-box .name-input,
.edit-box .type-input {
  margin-top: 10px;
  min-width: 180px;
}
.edit-box-btn-area {
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  margin-top: 20px;
}
.project .type {
  margin-top: 5px;
  font-size: 12px;
}
.btn-area {
  position: absolute;
  text-align: right;
  right: 10px;
  width: 200px;
  height: 60px;
  line-height: 60px;
  top: 0;
}
</style>
