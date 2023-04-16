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
            <p class="projectName">{{project.projectName}}</p>
            <p class="projectType">{{project.projectType}}</p>
            <div class="btn-area">
              <button class="button" @click="toNerAnno(project)">开始标注</button>
              <button class="button" @click="toEdit(project)">配置</button>
            </div>
          </div>
        </div>
      </div>
      <div v-if="page==='edit' || page==='create'" class="edit-box">
        <p>名称：<input class="name-input" type="text" name="name" @change="setName" :value="projectName" :disabled="page==='edit'"/></p>
        <p>类型：
          <select class="type-input" name="type" @change="setType" :value="projectType">
            <option value ="命名实体识别">命名实体识别</option>
            <option value ="文本分类">文本分类</option>
            <option value ="图片点标注">图片点标注</option>
            <option value ="人类反馈强化学习">人类反馈强化学习</option>
          </select>
        </p>
        <div class="title">
          <span>选择标签：</span>
          <br/>
          <div class="type-box">
            <span v-for="type in typeList" :key="type" @contextmenu="delType(type, $event)" class="type"
              :style="{
                backgroundColor: types[type] ? types[type].color : '#fff'
              }"
            >
              <svg t="1618942541356" @click.stop="clickColor(type, $event)" class="color-icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="1686" width="18" height="18"><path d="M204.4 524.9c-14.5 1.5-26.2 13.2-27.7 27.7-2.1 19.9 14.6 36.7 34.6 34.6 14.5-1.5 26.2-13.2 27.8-27.8 2-19.9-14.8-36.6-34.7-34.5zM265.4 473.7c21.8-1.9 39.4-19.5 41.4-41.4 2.5-28.5-21.2-52.3-49.7-49.7-21.8 1.9-39.4 19.5-41.4 41.4-2.6 28.4 21.2 52.2 49.7 49.7zM415.8 266.9c-28.5 1.8-51.6 24.9-53.4 53.4-2.2 34.5 26.4 63.1 60.9 60.9 28.5-1.8 51.6-24.9 53.4-53.4 2.1-34.6-26.4-63.1-60.9-60.9zM621.9 253.8c-35.1 2.2-63.4 30.6-65.6 65.6-2.7 42.4 32.4 77.6 74.8 74.8 35.1-2.2 63.4-30.6 65.6-65.6 2.8-42.4-32.3-77.5-74.8-74.8zM966.5 276.4c-0.5-7.6-4-14.6-9.8-19.6l-0.7-0.6c-5.2-4.5-11.9-7-18.8-7-8.3 0-16.2 3.6-21.6 9.9L574 652.4l-43.5 85.5 1.1 0.9-4.9 11.3 11.1-5.9 1.5 1.3 78-54.3 342.3-394c5-5.8 7.4-13.2 6.9-20.8z" p-id="1687" fill="#2c3e50"></path><path d="M897.8 476.3c-13.8-1.4-26.7 7.4-30.4 20.7-6.9 24.6-19.3 64.5-35.1 97.8C809.5 643 767.4 710.1 696.7 756c-72.2 46.9-142.7 56.7-189.2 56.7-37 0-72.2-6.1-101.7-17.7-26.9-10.5-46.4-24.6-54.9-39.7-3.4-6.1-7.2-12.9-11.2-20.2-17.2-31.1-36.6-66.5-49.7-77.4-15.9-13.2-39.1-15-59.8-15-8.1 0-40.8 1.3-48.5 1.3-33.1 0-49.4-6.5-56.1-22.4-17.8-42.3-7.3-114.3 26.8-183.4C205.2 331.4 300 253.3 412.6 224c40-10.6 81.2-18.9 121.3-18.9 85.6 0 187.8 32.8 252.5 77.2 11.4 7.8 26.9 5.8 35.7-4.9 10.4-12.6 7.1-31.4-6.8-39.8-23.3-14-57.9-34-86.3-47.1-60.3-27.9-123.7-41.9-189.2-41.9-68.1 0-148.8 16.4-217.2 47.2-78.1 35-135.2 85-179.4 147.5-36.4 51.4-67.8 111.1-80.1 168.7-7.5 35.1-6.8 57.4-2.4 87.8 4.2 29.2 13.4 52.5 26.9 67.5 22.4 25.1 51.5 37.4 89 37.4 13.9 0 56.3-5 63.1-5 7.4 0 12.2 1.2 14.4 3.8 6.4 7.4 14.4 22.4 23.7 39.9 7.5 14.1 15.9 30.1 25.4 45.3 12.1 19.5 36.9 40.4 66.5 55.9 27 14.1 71.9 31 132.2 31 72 0 148.3-23.6 226.7-70.1 74.9-44.4 123-118.9 150.2-173.6 19-38.3 34.7-87.2 43.8-119.1 4.8-17.3-7-34.7-24.8-36.5z" p-id="1688" fill="#2c3e50"></path></svg>
              <input :id="type" class="color-input" :value="types[type].color" type="color" @change="changeColor(type, $event)" @click.stop/>
              {{ type }}
              <svg t="1618943942999" class="close-icon" @click="checkDelType(type, $event)" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="3793" width="18" height="18"><path d="M512 421.504l274.752-274.752 90.496 90.496L602.496 512l274.752 274.752-90.496 90.496L512 602.496l-274.752 274.752-90.496-90.496L421.504 512 146.752 237.248l90.496-90.496z" p-id="3794" fill="#ff0000"></path></svg>
            </span>
            <span class="type-input-box">
              <input class="type-input" id="type-input" placeholder="新增标签" @keypress="typeInput" @change="typeInput"/>
              <button class="page-btn" @click="addType">提交</button>
            </span>
          </div>
        </div>
        <p>上传文本：</p>
        <p style="font-size:10px">（请选择包含文本文件的zip、tar文件）</p>
        <input type="file" id="file-input" accept=".zip,.tar,.jsonl,.txt"/>
        <p class="edit-box-btn-area">
          <button class="button danger" @click="del" v-if="page==='edit'">删除</button>
          <button class="button" @click="submit">提交</button>
          <button class="button" @click="toList">取消</button>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import { getColor } from '../../js/color'

function get (url, cb) {
  query('GET', url, '', cb)
}
function post (url, data, cb) {
  query('POST', url, data, cb)
}
function form (url, data, cb) {
  query('POST', url, data, cb, {
    contentType: 'multipart/form-data'
  })
}
function query (method, url, data = '', cb, config = {}) {
  var xhr = new XMLHttpRequest()
  xhr.open(method, url)
  if (!config.contentType) xhr.setRequestHeader('content-type', 'application/json')
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
  if (config.contentType === 'multipart/form-data') {
    xhr.send(data)
  } else {
    xhr.send(JSON.stringify(data))
  }
}

export default {
  name: 'home',
  data () {
    return {
      projects: [],
      projectName: '',
      projectType: '',
      page: 'list',
      types: {},
      typeList: []
    }
  },
  computed: {
  },
  watch: {
    projectName: console.log
  },
  methods: {
    goHome () {
      this.page = 'list'
    },
    setName (ev) {
      this.projectName = ev.target.value
    },
    setType (ev) {
      this.projectType = ev.target.value
    },
    del () {
      // 删除项目
      const that = this
      if (prompt(`请输入${this.projectName}来确认删除。`) === this.projectName) {
        get(`/v1/project/delete_program?projectName=${this.projectName}`, function () {
          that.init()
        })
      } else {
        alert('输入错误，删除失败')
      }
    },
    init () {
      // 初始化主页列表
      const that = this
      that.type = ''
      that.projectName = ''
      // 查询项目信息
      get('/v1/index', function (info) {
        that.$set(that, 'projects', info)
        that.projectName = ''
        that.projectType = ''
        that.page = 'list'
      })
    },
    submit () {
      const that = this
      const newEntityTypes = that.typeList.map((type) => {
        return {
          type,
          color: that.types[type].color
        }
      })
      const projectName = that.projectName
      post('/v1/project/create', {
        projectName: that.projectName,
        projectType: that.projectType,
        entityTypes: JSON.stringify(newEntityTypes)
      }, function () {
        that.init()
        // 如果有上传文件就更新文件
        const fileInputElement = document.getElementById('file-input')
        if (fileInputElement.files[0]) {
          let formData = new FormData()
          let file = fileInputElement.files[0]
          formData.append('projectName', projectName)
          formData.append('file', file)
          if (file.name.endsWith('.zip')) {
            form('/v1/project/get_zipped_data', formData)
          } else if (file.name.endsWith('.tar')) {
            form('/v1/project/get_zipped_data', formData)
          } else if (file.name.endsWith('.jsonl')) {
            form('/v1/project/get_jsonl_data', formData)
          } else if (file.name.endsWith('.txt')) {
            form('/v1/project/get_txt_data', formData)
          }
        }
      })
    },
    toNerAnno (project) {
      const { projectName, projectType, entityTypes } = project
      this.$router.push({path: '/NER', query: { projectName, projectType, entityTypes }})
    },
    toEdit (project = {}) {
      console.log('project', project)
      this.projectName = project.projectName || ''
      this.projectType = project.projectType || '命名实体识别' // 配置默认值
      this.page = project.projectName ? 'edit' : 'create'
      // 配置对应的实体类型配置
      const that = this
      const entityTypes = project.entityTypes ? JSON.parse(project.entityTypes) : []
      const types = {}
      that.typeList = entityTypes.map((entityType) => {
        types[entityType.type] = {
          color: entityType.color
        }
        return entityType.type
      })
      that.types = types
    },
    toList () {
      this.page = 'list'
    },
    /**
     * 增加类型
     * @param 类型
     */
    addType: function () {
      const that = this
      const newType = that.inputType
      document.getElementById('type-input').value = ''
      that.inputType = ''
      if (!newType) return false
      if (that.types[newType]) return false
      that.$set(that.types, newType, {
        color: getColor(that.types)
      })
      that.typeList.push(newType)
      console.log(that.typeList)
    },
    delType: function (type, ev) {
      const that = this
      ev && ev.preventDefault() // 取消默认的右键菜单事件
      // 右键删除对应的类型
      const newTypes = {}
      const newTypeList = []
      const { typeList, types } = that
      for (let i = 0; i < typeList.length; i++) {
        const srcType = typeList[i]
        if (type !== srcType) {
          newTypeList.push(srcType)
          newTypes[srcType] = types[srcType]
        }
      }
      that.typeList = newTypeList
      that.types = newTypes
    },
    checkDelType: function (type, ev) {
      ev && ev.stopPropagation()
      const isDel = window.confirm(`确定删除标签【${type}】么？`)
      if (isDel) {
        this.delType(type)
      }
    },
    typeInput: function (ev) {
      this.inputType = ev.target.value
      if (ev.code === 'Enter' || ev.code === 'NumpadEnter') {
        this.addType(ev)
      }
    },
    clickColor (type) {
      document.getElementById(type).click()
    },
    // 切换颜色
    changeColor (tarType, ev) {
      const that = this
      console.log(tarType, ev.target.value)
      that.$set(that.types[tarType], 'color', ev.target.value)
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
  margin: 0 10px;
  /* height: calc(100% - 92px); */
}
.button {
  color: #fff;
  background-color: #1161ca;
  border-radius: 4px;
  border: 1px solid #ccc;
  padding: 5px 10px;
}
.button.danger {
  background-color: #ff0000;
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
.project .projectName,
.project .projectType {
  margin: 0;
}
.edit-box {
  width: 280px;
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
.project .projectType {
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

.type-box {
  display: inline;
  line-height: 40px;
}
.type {
  display: block;
  position: relative;
  padding: 0px 10px;
  box-sizing: content-box;
  border: 1px solid #ccc;
  border-bottom: 3px solid #ccc;
}

.type {
  display: inline-block;
  margin-left: 10px;
  padding: 0 4px;
  min-width: 100px;
  height: 32px;
  font-size: 18px;
  line-height: 30px;
  border-radius: 4px;
  background: #eee;
  vertical-align: middle;
  outline:none;
}
.color-input {
  width: 0;
  height: 0;
  opacity: 0;
  pointer-events: none;
}
.color-icon {
  display: block;
  float: left;
  margin-top: 6px;
}
.close-icon {
  position: absolute;
  top: -9px;
  right: -9px;
}
</style>
