<template>
  <div>
    <span class="home" @click="goHome">whaleAnno</span>
    <h1 class="out-title">{{projectName}}（{{projectType}}）</h1>
    <div class="layout" @dragover="stopPrev" @drop="setFiles($event)">
      <div class="left">
        <div class="file-list">
          <div v-for="file in files" :key="file" @click="setNowText(file)"
            :class="['file', nowFile===file?'selected':'', nersCache[file]&&nersCache[file].length?'checked':'', ].join(' ')"
          >
            {{ file }}
          </div>
        </div>
        <div class="out-btn" @click="outAllNers">导出json结果</div>
      </div>
      <div class="right">
        <div class="title">
          <span>{{ nowFile }}</span>
          <div class="type-box">
            <span v-for="type in typeList" :key="type" @click="setType(type)" @contextmenu="delType(type, $event)" :class="nowType===type?'type selected':'type'"
              :style="{
                backgroundColor: types[type] ? types[type].color : '#fff'
              }"
              @mouseover="setFocus(type)"
              @mouseleave="setFocus('')"
            >
              <input class="color-input" :value="types[type].color" type="color" @change="changeColor(type, $event)" @click.stop/>
              {{ type }} {{ fastTypeKey[type] ? `【${fastTypeKey[type]}】` : '' }}
            </span>
            <input class="type-input" placeholder="新增标签" @blur="addType" @keypress="typeInput"/>
          </div>
        </div>
        <div id="ner-box" class="ner-box" @mouseup="setMode('')" @mouseleave="setMode('');setFocus('')" @keydown="setTypeByFastKey" @mouseover="setFocus('ner-box')">
          <div class="word-rect-area">
            <span class="rect" v-for="(word, idx) in nowNers" :key="idx">
              <span v-for="(w, i) in word.name" :key="`${word}${w}${i}`">
                <!-- <span class="ner-type"
                  v-if="i===0"
                  :style="{
                    left: `${((word.start+i)%columnWordCount)*20}px`,
                    top:  `${((word.start+i)/columnWordCount|0)*35 - 14}px`,
                  }"
                >{{word.type}}</span> -->
                <span class="ner-anchor"
                  v-if="i === 0 || ((word.start%columnWordCount)+i) % columnWordCount === 0"
                  :style="{
                  border: '1px solid #ccc',
                  position: 'absolute',
                  display: 'inline-block',
                  left: `${((word.start+i)%columnWordCount)*20 + (word.isSmall && i === 0 ? 2 : 0)}px`,
                  top:  `${((word.start+i)/columnWordCount|0)*35 + (word.isSmall ? 0 : -2)}px`,
                  width: `${(Math.min(word.end-(word.start+i), columnWordCount, columnWordCount - (word.start+i)%columnWordCount))*20 - (word.isSmall && i === 0 ? 4 : 0)}px`,
                  height: `${word.isSmall?18:22}px`,
                  background: `${types[word.type]?types[word.type]['color']:'000000'}`,
                  lineHeight: '25px',
                  borderTopLeftRadius: `${(i===0)?6:0}px`,
                  borderBottomLeftRadius: `${(i===0)?6:0}px`,
                  borderLeft: `${i===0?1:0} solid #ccc`,
                  borderTopRightRadius: `${(i!==0 && word.name.length-i <= columnWordCount) || (i===0 && word.start%columnWordCount+word.name.length <= columnWordCount)?6:0}px`,
                  borderBottomRightRadius: `${(i!==0 && word.name.length-i <= columnWordCount) || (i===0 && word.start%columnWordCount+word.name.length <= columnWordCount)?6:0}px`,
                  borderRight: `${(i!==0 && word.name.length-i <= columnWordCount) || (i===0 && word.start%columnWordCount+word.name.length < columnWordCount)?1:0} solid #ccc`
                }"></span>
              </span>
            </span>
          </div>
          <span class="word" v-for="(word, idx) in nowText" :key="idx" @contextmenu="stopPrev" @mousedown="startSelect(idx, $event)" @mousemove="pointWord(idx)"
          >
            {{ word }}
          </span>
        </div>
        <div class="page-btn-box">
          <button class="page-btn" @click="changePage(-1)" @mouseover="setFocus('page-up')" @mouseleave="setFocus('')">上一页 {{ fastTypeKey['page-up'] ? `【${fastTypeKey['page-up']}】` : '' }}</button>
          <button class="page-btn" @click="changePage(+1)" @mouseover="setFocus('page-down')" @mouseleave="setFocus('')">下一页 {{ fastTypeKey['page-down'] ? `【${fastTypeKey['page-down']}】` : '' }}</button>
          <button class="page-btn"
            :disabled="!nersCache[nowFile] || JSON.stringify(nersCache[nowFile]) === JSON.stringify(ners)"
            @click="save" @mouseover="setFocus('save')" @mouseleave="setFocus('')"
          >保存 {{ fastTypeKey['save'] ? `【${fastTypeKey['save']}】` : '' }}</button>
        </div>
      </div>
      <div class="result-box">
        <div class="result" v-for="(ner, idx) in ners" :key="idx"
          :class="nowType===ner.type?'result selected':'result'"
          :style="{
            backgroundColor: types[ner.type] ? types[ner.type].color : `#fff`,
          }"
        >
          <span class="result-type">{{ ner.type }}</span>
          <span class="result-name">{{ ner.name }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
function getColor () {
  const idxs = '0123456789abcdef'
  let color = '#'
  for (let i = 0; i < 6; i += 1) {
    color += idxs[Math.random() * idxs.length | 0]
  }
  return color
}

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
get('/v1/index', function (data) {
  console.log('data', data)
})
function updateType2Server (projectName, typeList, types) {
  const entityTypes = typeList.map((type) => {
    return {
      type,
      color: types[type].color
    }
  })
  post('/v1/project/update_entity_types', {
    projectName: projectName,
    entityTypes: JSON.stringify(entityTypes)
  })
}

export default {
  name: 'NER',
  data () {
    return {
      projectName: '', // 项目名称
      projectType: '', // 项目类型
      columnWordCount: 10, // 每列的字数，会自动计算
      files: [ // 文件列表
      ],
      textDic: { // 文件名对应的文本
      },
      startIdx: -1, // 标注起始位置，鼠标按下后触发联动
      endIdx: -1, // 标注结束位置（最后的end需要为endIdx+1），鼠标按下后触发联动
      nowFile: '', // 当前在编辑的文件名
      nowText: '', // 当前的文件文本
      ners: [], // 当前文件已标注的实体
      nowNer: {}, // 当前鼠标正在标注的实体
      nowType: 'person', // 当前选择的实体类型
      typeList: ['person', 'location', 'organiztion'], // 实体类型可选列表
      nowFocus: '', // 鼠标当前位置的对象，比如标注框/类型按钮/翻页按钮
      fastKeyType: {}, // 快捷键对应的类型
      fastTypeKey: {}, // 类型对应的快捷键
      types: { // 类型对应的属性
        'person': {
          color: '#e61490'
        },
        'location': {
          color: '#0aab8a'
        },
        'organiztion': {
          color: '#2770cd'
        }
      },
      wordsType: [], // 文字对应的标注
      // 嵌套实体，外部放大
      wordsOutType: [], // 文字对应是否放大
      nersCache: { // 各个文件已标注内容的缓存
      },
      mode: '' // 如果鼠标在文字上按下了，就开始'select'模式，开始框选实体
    }
  },
  computed: {
    wordColor: function (...args) {
      return '#ff0000'
    },
    nowNers: function () {
      if (this.nowNer) {
        return [...this.ners, this.nowNer]
      }
      return this.ners
    }
  },
  methods: {
    goHome: function () {
      this.$router.push({path: '/'})
    },
    save: function () {
      const that = this
      // 保存当前标注
      post('/v1/anno/create', {
        projectName: that.projectName,
        fileName: that.nowFile,
        annoDetails: JSON.stringify(that.ners)
      })
      that.$set(that.nersCache, that.nowFile, [...that.ners])
    },
    /**
     * 选中目标文件
     * @param name 文件名
     */
    setNowText: function (newFile) {
      const that = this
      that.save()
      that.nowFile = newFile
      that.nowText = that.textDic[newFile]
      const hasCache = !!that.nersCache[newFile]
      that.$set(that, 'ners', that.nersCache[newFile] ? [...that.nersCache[newFile]] : [])
      that.flushWordsType()
      get(`/v1/anno/query?projectName=${that.projectName}&fileName=${newFile}`, function (info) {
        // 如果本地没有缓存，就用线上的标注记录
        if (!hasCache && info.annoDetails) {
          that.$set(that, 'ners', JSON.parse(info.annoDetails))
          that.$set(that.nersCache, that.nowFile, [...that.ners])
          that.flushWordsType()
        }
        // 更新文件的文本信息
        that.$set(that.textDic, newFile, info.fileContent)
        that.nowText = that.textDic[newFile]
      })
    },
    changePage: function (d) {
      const nowIdx = this.files.indexOf(this.nowFile)
      let newIdx = nowIdx + d
      if (newIdx < 0) newIdx = 0
      if (newIdx >= this.files.length) newIdx = this.files.length - 1
      this.setNowText(this.files[newIdx])
    },
    /**
     * 标注文本
     * @param idx 点击文字的定位
     */
    pointWord: function (idx, config = {}) {
      if (this.mode === 'select') {
        this.endIdx = idx
        const type = this.nowType
        const start = Math.min(this.startIdx, this.endIdx)
        const end = Math.max(this.startIdx, this.endIdx) + 1
        const name = this.nowText.substring(start, end)
        this.$set(this, 'nowNer', { name, type, start, end, isMove: !config.isDefaultClick })
        return idx
      }
    },
    /**
     * 配置标注类型
     * @param 类型
     */
    setType: function (type, ev) {
      this.$set(this, 'nowType', type)
    },
    delType: function (type, ev) {
      const that = this
      ev.preventDefault() // 取消默认的右键菜单事件
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
      that.flushWordsType()
      updateType2Server(that.projectName, that.typeList, that.types)
    },
    /**
     * 增加类型
     * @param 类型
     */
    addType: function (ev) {
      const that = this
      const newType = ev.target.value
      ev.target.value = ''
      if (!newType) return false
      if (that.types[newType]) return false
      that.$set(that.types, newType, {
        color: getColor()
      })
      that.typeList.push(newType)
      updateType2Server(that.projectName, that.typeList, that.types)
    },
    typeInput: function (ev) {
      if (ev.code === 'Enter' || ev.code === 'NumpadEnter') {
        this.addType(ev)
      }
    },
    setMode: function (mode) {
      // 如果之前是选择模式，就取消选择
      if (this.mode === 'select') {
        this.endSelect()
      }
      this.mode = mode
    },
    flushWordsType: function () {
      const ners = JSON.parse(JSON.stringify(this.ners))
      if (this.nowNer) ners.push(this.nowNer)
      this.wordsType = []
      for (let i = 0; i < ners.length; i += 1) {
        const ner = ners[i]
        for (let j = ner.start; j < ner.end; j += 1) {
          this.wordsType[j] = ner.type
        }
      }
      this.$set(this, 'wordsType', this.wordsType)
      // 展示实体嵌套外部框
      this.wordsOutType = []
      for (let i = 0; i < ners.length; i += 1) {
        const ner = ners[i]
        let isNeedOut = false
        for (let j = ner.start; j < ner.end; j += 1) {
          if (ner.type !== this.wordsType[j]) {
            isNeedOut = true
            break
          }
        }
        if (isNeedOut) {
          for (let j = ner.start; j < ner.end; j += 1) {
            this.wordsOutType[j] = ner.type
          }
        }
      }
      this.$set(this, 'wordsOutType', this.wordsOutType)
    },
    startSelect: function (idx, event) {
      if (event.which === 3) {
        event.preventDefault()
        // 右键删除对应的图标
        const ners = this.ners
        for (let i = ners.length - 1; i >= 0; i -= 1) {
          const ner = ners[i]
          if (idx >= ner.start && idx < ner.end) {
            ners.splice(i, 1)
            this.$set(this, 'ners', ners)
            this.flushWordsType()
            return true
          }
        }
        return true
      }
      this.setMode('select')
      this.$set(this, 'nowNer', {})
      this.startIdx = idx
      this.endIdx = idx
      this.pointWord(idx, {isDefaultClick: true})
    },
    checkIsRepeat: function (tarNer) {
      for (let i = 0; i < this.ners.length; i += 1) {
        const ner = this.ners[i]
        if (ner.start === tarNer.start && ner.end === tarNer.end) {
          return true
        }
      }
      return false
    },
    endSelect: function () {
      const isRepeat = this.checkIsRepeat(this.nowNer)
      if (!isRepeat && this.nowNer.isMove) {
        delete this.nowNer.isMove
        this.ners.push(this.nowNer)
        this.$set(this, 'ners', this.ners.sort((a, b) => {
          return (a.start - b.start) + (b.end - a.end) * 0.001
        }))
      }
      this.$set(this, 'nowNer', undefined)
      this.flushWordsType()
      this.startIdx = -1
    },
    stopPrev: function (event) {
      event.preventDefault()
    },
    setFiles: function (event) {
      // 取消事件传播及默认行为
      event.stopPropagation()
      event.preventDefault()
      // 取得拖进来的文件
      var data = event.dataTransfer
      var files = data.files
      // 将其传给真正的处理文件的函数
      this.processFiles(files)
    },
    processFiles: function (files) {
      var that = this
      that.$set(that, 'files', [])
      that.$set(that, 'textDic', {})
      for (let i = 0; i < files.length; i += 1) {
        const file = files[i]
        // 创建FileReader
        const reader = new FileReader()
        // 告诉它在准备好数据之后做什么
        reader.onload = function (e) {
          // 使用图像URL来绘制dropBox的背景
          // dropBox.style.backgroundImage = "url('" + e.target.result + "')";
          // 更新文本信息
          that.$set(that.files, i, file.name)
          that.$set(that.textDic, file.name, e.target.result)
        }
        // 读取图片
        // reader.readAsDataURL(file)
        // 读取文件
        reader.readAsText(file, 'UTF-8')
        // reader.readAsText(file, 'GB2321')
      }
    },
    outAllNers () {
      this.nersCache[this.nowFile] = this.ners
      const out = []
      for (const fileName in this.nersCache) {
        const file = fileName
        const text = this.textDic[fileName]
        const entity = this.nersCache[fileName]
        out.push({ file, text, entity })
      }
      this.saveTxt(`${Date.now()}.json`, JSON.stringify(out))
    },
    saveTxt (fileName, content) {
      var element = document.createElement('a')
      element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(content))
      element.setAttribute('download', fileName)
      element.style.display = 'none'
      document.body.appendChild(element)
      element.click()
      document.body.removeChild(element)
    },
    setFastKey (event) {
      console.log(event)
    },
    setTypeByFastKey (event) {
      console.log(event)
    },
    setFocus (tar) {
      this.nowFocus = tar
    },
    // 切换颜色
    changeColor (tarType, ev) {
      const that = this
      console.log(tarType, ev.target.value)
      that.$set(that.types[tarType], 'color', ev.target.value)
      updateType2Server(that.projectName, that.typeList, that.types)
    }
  },
  watch: {
    ners: function () {
      // 给ner加上是否缩小的属性
      let nowSmallAreaEnd
      for (let i = 0; i < this.ners.length; i++) {
        const ner = this.ners[i]
        ner.isSmall = false
        if (nowSmallAreaEnd) {
          if (ner.start <= nowSmallAreaEnd) {
            ner.isSmall = true
          }
        }
        if (!nowSmallAreaEnd) nowSmallAreaEnd = ner.end - 1
        nowSmallAreaEnd = Math.max(nowSmallAreaEnd, ner.end - 1)
      }
    }
  },
  mounted () {
    const that = this
    console.log(that.$route)
    const { projectName, projectType, entityTypes } = that.$route.query
    if (projectName) {
      that.projectName = projectName
      that.projectType = projectType
      // 配置对应的实体类型配置
      that.entityTypes = entityTypes ? JSON.parse(entityTypes) : []
      const types = {}
      that.typeList = that.entityTypes.map((entityType) => {
        types[entityType.type] = {
          color: entityType.color
        }
        return entityType.type
      })
      that.types = types
      get(`/v1/files/query?projectName=${projectName}&pageNumber=1&pageSize=99999999`, function (info) {
        that.$set(that, 'files', info)
      })
    }
    function calcColumnWordCount () {
      const nerBox = document.getElementById('ner-box')
      const nerBoxWidth = nerBox.offsetWidth
      return (nerBoxWidth - 2 * 15) / 20 | 0
    }
    that.$set(that, 'columnWordCount', calcColumnWordCount())
    window.onresize = function () {
      that.$set(that, 'columnWordCount', calcColumnWordCount())
    }
    // 监听键盘事件，用于配置快捷键
    window.onkeydown = function (ev) {
      if (that.nowFocus) {
        const { key } = ev
        if (that.nowFocus === 'ner-box') {
          // 用于选择对应的类型
          const type = that.fastKeyType[key]
          if (type) {
            if (type === 'page-up') {
              // 快捷上一页
              that.changePage(-1)
            } else if (type === 'page-down') {
              // 快捷下一页
              that.changePage(+1)
            } else if (type === 'save') {
              // 保存
              that.save()
            } else {
              // 快捷选择类型
              const type = that.fastKeyType[key]
              that.setType(type)
            }
          }
        } else {
          // 删除旧的快捷键
          const oldKey = that.fastTypeKey[that.nowFocus]
          if (oldKey) {
            that.$set(that.fastKeyType, oldKey, undefined)
          }
          // 保存新的快捷键
          that.$set(that.fastKeyType, key, that.nowFocus)
          // 计算新的 类型->键 关系
          const typeKey = {}
          for (const key in that.fastKeyType) {
            const type = that.fastKeyType[key]
            typeKey[type] = key
          }
          that.$set(that, 'fastTypeKey', typeKey)
        }
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.home {
  position: absolute;
  top: 0;
  left: 0;
  padding: 5px 10px;
  color: #fff;
  cursor: pointer;
}
.home:hover {
  opacity: .6;
}
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
.layout {
  display: flex;
  flex-direction: row;
  height: calc(100% - 92px);
}
.title {
  padding: 0 12px;
  text-align: left;
}
.left {
  position: relative;
  color: white;
  width: 120px;
  background: #054ba8;
}
.left .file {
  margin: 12px 0;
  cursor: pointer;
}
.left .file.checked {
  color: #ccc;
}
.left .file.selected {
  background: #033271;
  z-index: 5;
}
.left .file-list {
  overflow: auto;
  height: calc(100% - 41px);
}
.left .out-btn {
  position: absolute;
  display: inline-block;
  bottom: 0;
  left: 0;
  right: 0;
  height: 41px;
  line-height: 41px;
  vertical-align: middle;
  margin: auto;
  cursor: pointer;
  background: #054ba8;
}
.left .out-btn:hover {
  opacity: .6;
}
.right {
  padding: 12px 0;
  display: flex;
  flex: 1;
  flex-direction: column;
  user-select: none;
}
.type-box {
  display: inline;
  line-height: 40px;
}
.type,
.type-input,
.page-btn {
  display: inline-block;
  margin-left: 10px;
  padding: 0 4px;
  min-width: 100px;
  height: 32px;
  font-size: 18px;
  line-height: 30px;
  border-radius: 4px;
  background: #eee;
  /* opacity: .6; */
  vertical-align: middle;
  outline:none;
}
.page-btn {
  cursor: pointer;
  opacity: 1;
}
.page-btn:active {
  opacity: 0.6;
}

.type-input {
  width: 100px;
  background: white;
}
.type {
  box-sizing: content-box;
  /* box-shadow: 2px 2px 0px #ccc; */
  border: 1px solid #ccc;
  border-bottom: 3px solid #ccc;
}
.type.selected,
.result.selected {
  position: relative;
  opacity: 1 !important;
  background: white;
  border: 0;
}
.type.selected {
  transform: translateX(0px) translateY(2px);
  border: 1px solid #ccc;
  border-bottom: 1px solid #ccc;
}
.ner-box {
  position: relative;
  flex: 1;
  padding: 14px;
  margin: 14px;
  border: 1px solid #ccc;
  text-align: left;
  /* font-size: 0; */
}
.ner-box .word {
  display: inline-block;
  position: relative;
  margin-bottom: 15px;
  width: 20px;
  height: 20px;
  line-height: 20px;
  vertical-align: bottom;
  box-sizing: border-box;
  text-align: center;
  font-size: 16px;
  z-index: 4;
}
.ner-box .ner-type {
  position: absolute;
  top: -14px;
  left: 0;
  font-size: 12px;
  line-height: 15px;
  vertical-align: bottom;
  z-index: 1;
  word-break: keep-all;
  background: white;
}
.ner-box .ner-anchor {
  z-index: 2;
}
.result-box {
  width: 120px;
}
.result {
  overflow: hidden;
  padding: 0 4px;
  height: 22px;
  text-align: left;
}
.result-type,
.result-name {
  width: 30%;
  display: inline-block;
  overflow: hidden;
  vertical-align: top;
  line-height: 22px;
}
.result-name {
  width: calc(100% - 30% - 8px);
}

.word-rect-area {
  position: absolute;
  top: 14px;
  right: 14px;
  left: 14px;
  bottom: 14px;
  z-index: 3;
  pointer-events: none;
}

.word-rect-area .rect {
  position: absolute;
  pointer-events: none;
}

.color-input {
  margin: 0;
  outline: none;
  border: 0px;
  padding: 0;
  width: 18px;
  height: 22px;
  line-height: 32px;
  background-color: #0000;
}
</style>
