<template>
  <div class="layout">
    <span class="home" @click="goHome">whaleAnno</span>
    <span class="now-file">{{ nowFile }}</span>
    <h1 class="out-title"><span class="out-title-span">{{projectName}}（{{projectType}}）</span></h1>
    <div class="container" @dragover="stopPrev" @drop="setFiles($event)">
      <div class="left">
        <div class="file-list" id="file-list">
          <div v-for="file in files" :key="file" :id="file" @click="setNowText(file)"
            :title=file
            :class="['file', nowFile===file?'selected':'', isAnnoDic[`${projectName}_${file}`]||(nersCache[file]&&nersCache[file].length)?'checked':'', ].join(' ')"
          >
            {{ file }}
            <svg v-if="isAnnoDic[`${projectName}_${file}`]||(nersCache[file]&&nersCache[file].length)" t="1619449859327" class="checked-icon" viewBox="0 0 1152 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="1159" width="16" height="16"><path d="M4.266667 576l238.933333-187.733333 204.8 192c0 0 379.733333-328.533333 699.733333-512l0 123.733333C704 580.266667 426.666667 989.866667 426.666667 989.866667L4.266667 576 4.266667 576zM4.266667 576" p-id="1160" fill="#35e558"></path></svg>
          </div>
          <div class="process-bar" :style="{width: `${processRate*100}%`}"></div>
        </div>
        <div class="page-ctl">
          <span class="page-ctl-last" :style="{opacity: pageNumber === 1 || isLoadingPage ? 0 : 1}" @click="lastPage">上页</span>
          <span class="page-number" :style="{opacity: (pageNumber === 1 || isLoadingPage) && files.length < pageSize ? 0 : 1}">{{pageNumber}}</span>
          <span class="page-ctl-next" :style="{opacity: files.length < pageSize ? 0 : 1}" @click="nextPage">下页</span>
        </div>
        <div class="out-btn" @click="outAllNers">导出json结果</div>
      </div>
      <div class="right">
        <div class="title">
          <span>选择标签：</span>
          <button v-if="projectType === '图片点标注'" @click="autoAnno" class="auto-anno">自动标注</button>
          <div class="type-box">
            <span v-for="type in typeList" :key="type" @click="setType(type)" @contextmenu="delType(type, $event)" :class="isTypeSelected(type)?'type selected':'type'"
              :style="{
                backgroundColor: types[type] ? types[type].color : '#fff'
              }"
              @mouseover="setFocus(type)"
              @mouseleave="setFocus('')"
            >
              <svg v-if="configCanCtlType" t="1618942541356" @click.stop="clickColor(type, $event)" class="color-icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="1686" width="18" height="18"><path d="M204.4 524.9c-14.5 1.5-26.2 13.2-27.7 27.7-2.1 19.9 14.6 36.7 34.6 34.6 14.5-1.5 26.2-13.2 27.8-27.8 2-19.9-14.8-36.6-34.7-34.5zM265.4 473.7c21.8-1.9 39.4-19.5 41.4-41.4 2.5-28.5-21.2-52.3-49.7-49.7-21.8 1.9-39.4 19.5-41.4 41.4-2.6 28.4 21.2 52.2 49.7 49.7zM415.8 266.9c-28.5 1.8-51.6 24.9-53.4 53.4-2.2 34.5 26.4 63.1 60.9 60.9 28.5-1.8 51.6-24.9 53.4-53.4 2.1-34.6-26.4-63.1-60.9-60.9zM621.9 253.8c-35.1 2.2-63.4 30.6-65.6 65.6-2.7 42.4 32.4 77.6 74.8 74.8 35.1-2.2 63.4-30.6 65.6-65.6 2.8-42.4-32.3-77.5-74.8-74.8zM966.5 276.4c-0.5-7.6-4-14.6-9.8-19.6l-0.7-0.6c-5.2-4.5-11.9-7-18.8-7-8.3 0-16.2 3.6-21.6 9.9L574 652.4l-43.5 85.5 1.1 0.9-4.9 11.3 11.1-5.9 1.5 1.3 78-54.3 342.3-394c5-5.8 7.4-13.2 6.9-20.8z" p-id="1687" fill="#2c3e50"></path><path d="M897.8 476.3c-13.8-1.4-26.7 7.4-30.4 20.7-6.9 24.6-19.3 64.5-35.1 97.8C809.5 643 767.4 710.1 696.7 756c-72.2 46.9-142.7 56.7-189.2 56.7-37 0-72.2-6.1-101.7-17.7-26.9-10.5-46.4-24.6-54.9-39.7-3.4-6.1-7.2-12.9-11.2-20.2-17.2-31.1-36.6-66.5-49.7-77.4-15.9-13.2-39.1-15-59.8-15-8.1 0-40.8 1.3-48.5 1.3-33.1 0-49.4-6.5-56.1-22.4-17.8-42.3-7.3-114.3 26.8-183.4C205.2 331.4 300 253.3 412.6 224c40-10.6 81.2-18.9 121.3-18.9 85.6 0 187.8 32.8 252.5 77.2 11.4 7.8 26.9 5.8 35.7-4.9 10.4-12.6 7.1-31.4-6.8-39.8-23.3-14-57.9-34-86.3-47.1-60.3-27.9-123.7-41.9-189.2-41.9-68.1 0-148.8 16.4-217.2 47.2-78.1 35-135.2 85-179.4 147.5-36.4 51.4-67.8 111.1-80.1 168.7-7.5 35.1-6.8 57.4-2.4 87.8 4.2 29.2 13.4 52.5 26.9 67.5 22.4 25.1 51.5 37.4 89 37.4 13.9 0 56.3-5 63.1-5 7.4 0 12.2 1.2 14.4 3.8 6.4 7.4 14.4 22.4 23.7 39.9 7.5 14.1 15.9 30.1 25.4 45.3 12.1 19.5 36.9 40.4 66.5 55.9 27 14.1 71.9 31 132.2 31 72 0 148.3-23.6 226.7-70.1 74.9-44.4 123-118.9 150.2-173.6 19-38.3 34.7-87.2 43.8-119.1 4.8-17.3-7-34.7-24.8-36.5z" p-id="1688" fill="#2c3e50"></path></svg>
              <input v-if="configCanCtlType" :id="type" class="color-input" :value="types[type].color" type="color" @change="changeColor(type, $event)" @click.stop/>
              {{ type }} {{ fastTypeKey[type] ? `【${fastTypeKey[type]}】` : '' }}
              <svg v-if="configCanCtlType" t="1618943942999" class="close-icon" @click="checkDelType(type, $event)" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="3793" width="18" height="18"><path d="M512 421.504l274.752-274.752 90.496 90.496L602.496 512l274.752 274.752-90.496 90.496L512 602.496l-274.752 274.752-90.496-90.496L421.504 512 146.752 237.248l90.496-90.496z" p-id="3794" fill="#ff0000"></path></svg>
            </span>
            <span v-if="configCanCtlType" class="type-input-box">
              <input class="type-input" id="type-input" placeholder="新增标签" @keypress="typeInput" @change="typeInput"/>
              <button class="page-btn" @click="addType">提交</button>
            </span>
          </div>
        </div>
        <div id="ner-box" class="ner-box" @mouseup="setMode('')" @touchend="setMode('')" @mouseleave="setMode('');setFocus('')" @keydown="setTypeByFastKey" @mouseover="setFocus('ner-box')">
          <!-- <svg style=" position: absolute; z-index: 99999999; overflow: unset; pointer-events: none">
          <template class="rect" v-for="(word, idx) in nowNers" >
            <template v-for="(w, i) in word.name">
              <line
              v-if="i === 0 || ((word.start%columnWordCount)+i) % columnWordCount === 0"
              :key="`${word}${w}${i}`"
                :x1="`${((word.start+i)%columnWordCount)*20 + (word.isSmall && i === 0 ? 2 : 0)}px`"
                :y1="`${((word.start+i)/columnWordCount|0)*35 + (word.isSmall ? 0 : -2)}px`"
                :x2="`${((Math.min(word.end-(word.start+i), columnWordCount, columnWordCount - (word.start+i)%columnWordCount))*20 - (word.isSmall && i === 0 ? 4 : 0)) + ((word.start+i)%columnWordCount)*20 + (word.isSmall && i === 0 ? 2 : 0)}px`"
                :y2="`${word.isSmall?18:22+((word.start+i)/columnWordCount|0)*35 + (word.isSmall ? 0 : -2)}px`"
                style="stroke:rgb(255,0,0);stroke-width:2"
              ></line>
              </template>
            </template>
          </span>
            <text x="201" y="10" fill="red">关系一</text>
          </svg> -->
          <div v-if="nerProjectType.indexOf(projectType) > -1">
            <span class="word" v-for="(word, idx) in nowText" :key="idx" :id="idx" @contextmenu="stopPrev" @mousedown="startSelect(idx, $event)" @touchstart="startSelect(idx, $event)" @touchend="stopSelect()" @mousemove="pointWord(idx)" @touchmove="pointWordByTouch($event)"
            >
              {{ word }}
            </span>
          </div>
          <div v-if="nerProjectType.indexOf(projectType) > -1">
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
          </div>
          <div v-if="projectType === '文本分类'">
            <template v-for="(word, idx) in nowText">
              <span class="word" v-if="word !== '\n'" :key="idx" @contextmenu="stopPrev" @mousedown="startSelect(idx, $event)" @mousemove="pointWord(idx)">{{ word }}</span>
              <br v-if="word === '\n'" :key="idx"/>
            </template>
          </div>
          <CVPoint v-if="projectType === '图片点标注'" :fileContent="nowText" :annoDetails="ners" :nowType="nowType" :types="types" :save="save"></CVPoint>
          <RLHF v-if="projectType === '人类反馈强化学习'" :fileContent="nowText" :annoDetails="ners" :nowType="nowType" :types="types" :save="save"></RLHF>
          <Rel v-if="projectType === '关系标注'" :relDetails="relDetails" :nowType="nowType" :types="types" :save="save"></Rel>
        </div>
        <div class="page-btn-box">
          <button class="page-btn" @click="changeIdx(-1, $event)" @mouseover="setFocus('page-up')" @mouseleave="setFocus('')">上一个 {{ fastTypeKey['page-up'] ? `【${fastTypeKey['page-up']}】` : '' }}</button>
          <button class="page-btn" @click="changeIdx(+1, $event)" @mouseover="setFocus('page-down')" @mouseleave="setFocus('')">下一个 {{ fastTypeKey['page-down'] ? `【${fastTypeKey['page-down']}】` : '' }}</button>
        </div>
      </div>
      <div class="result-box">
        <div class="result" v-for="(ner, idx) in ners" :key="idx"
          :class="nowType===ner.type?'result selected':'result'"
          :style="{
            backgroundColor: types[ner.type] ? types[ner.type].color : `#fff`,
          }"
        >
          <span class="result-name">{{ ner.name }}
            <svg t="1649340286830" class="result-name-del" @click="del(idx)" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="5736" width="17" height="17"><path d="M916.945455 251.345455H768V190.836364c0-48.872727-39.563636-90.763636-88.436364-90.763637h-302.545454c-48.872727 0-90.763636 39.563636-90.763637 90.763637v60.509091H137.309091c-16.290909 0-30.254545 13.963636-30.254546 30.254545 0 16.290909 13.963636 30.254545 30.254546 30.254545h777.309091c16.290909 0 30.254545-13.963636 30.254545-30.254545 0-16.290909-11.636364-30.254545-27.927272-30.254545zM346.763636 190.836364c0-16.290909 13.963636-30.254545 30.254546-30.254546h300.218182c16.290909 0 30.254545 13.963636 30.254545 30.254546v60.509091H346.763636V190.836364z m0 0M646.981818 730.763636V400.290909c0-16.290909-13.963636-30.254545-30.254545-30.254545-16.290909 0-30.254545 13.963636-30.254546 30.254545v328.145455c0 16.290909 13.963636 30.254545 30.254546 30.254545 16.290909 2.327273 30.254545-11.636364 30.254545-27.927273z m0 0M467.781818 730.763636V400.290909c0-16.290909-13.963636-30.254545-30.254545-30.254545-16.290909 0-30.254545 13.963636-30.254546 30.254545v328.145455c0 16.290909 13.963636 30.254545 30.254546 30.254545 16.290909 2.327273 30.254545-11.636364 30.254545-27.927273z m0 0" p-id="5737" fill="#d81e06"></path><path d="M795.927273 372.363636c-16.290909 0-30.254545 13.963636-30.254546 30.254546v449.163636c0 16.290909-13.963636 30.254545-30.254545 30.254546h-418.909091c-16.290909 0-30.254545-13.963636-30.254546-30.254546V400.290909c0-16.290909-13.963636-30.254545-30.254545-30.254545-16.290909 0-30.254545 13.963636-30.254545 30.254545v449.163636c0 48.872727 39.563636 90.763636 90.763636 90.763637h418.909091c48.872727 0 90.763636-39.563636 90.763636-90.763637V402.618182c0-16.290909-13.963636-30.254545-30.254545-30.254546z m0 0" p-id="5738" fill="#d81e06"></path></svg>
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getColor } from '../../js/color.js'
import CVPoint from '@/components/CV/point.vue'
import RLHF from '@/components/NLP/rlhf.vue'
import Rel from '@/components/NLP/rel.vue'

// 是否是单机版
const isLocal = false

function get (url, cb, config = {}) {
  query('GET', url, '', cb, config)
}
function post (url, data, cb, config = {}) {
  query('POST', url, data, cb, config)
}
function query (method, url, data = '', cb, config = {}) {
  config.tryTimes = config.tryTimes || 0
  config.isDirect = config.isDirect || false

  var xhr = new XMLHttpRequest()
  xhr.open(method, url)
  xhr.setRequestHeader('content-type', 'application/json')
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
      if (config.isDirect) {
        return cb(xhr.responseText) // 直接返回请求结果
      }
      const result = JSON.parse(xhr.responseText)
      if (result.errCode !== 0) {
        if (config.tryTimes >= 2) {
          alert(result.errMsg)
        } else {
          setTimeout(() => {
            config.tryTimes += 1
            query(method, url, data, cb, config)
          }, 200)
        }
      } else {
        cb && cb(result.info)
      }
    }
  }
  xhr.send(JSON.stringify(data))
}
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
  components: {
    CVPoint,
    RLHF,
    Rel
  },
  data () {
    return {
      configCanCtlType: isLocal, // 是否支持实体类型的调整
      pageNumber: 1,
      pageSize: 20,
      isLoadingPage: false,
      inputType: '',
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
      nowType: '', // 当前选择的实体类型
      typeList: ['person', 'location', 'organiztion'], // 实体类型可选列表
      isAnnoDic: {}, // 服务器是否返回已标注过
      nowFocus: '', // 鼠标当前位置的对象，比如标注框/类型按钮/翻页按钮
      fastKeyType: localStorage.fastKeyType ? JSON.parse(localStorage.fastKeyType) : {}, // 快捷键对应的类型
      fastTypeKey: localStorage.fastTypeKey ? JSON.parse(localStorage.fastTypeKey) : {}, // 类型对应的快捷键
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
      mode: '', // 如果鼠标在文字上按下了，就开始'select'模式，开始框选实体
      nerProjectType: ['命名实体识别', '关系标注'],
      relStartIdx: '',
      relDetails: []
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
    },
    processRate: function () {
      const files = this.files || []
      if (!files.length) return 0
      const nersCache = this.nersCache || {}
      const projectName = this.projectName || ''
      const isAnnoDic = this.isAnnoDic || {}
      let cnt = 0
      for (let i = 0; i < files.length; i += 1) {
        const file = files[i]
        if (isAnnoDic[`${projectName}_${file}`] || (nersCache[file] && nersCache[file].length)) {
          cnt += 1
        }
      }
      return cnt / files.length
    }
  },
  methods: {
    log (...args) {
      console.log(args)
    },
    // 获取文件列表
    getFiles () {
      const that = this
      that.isLoadingPage = true
      get(`/v1/files/query?projectName=${that.projectName}&pageNumber=${that.pageNumber}&pageSize=${that.pageSize}`, function (info) {
        that.isLoadingPage = false
        if (!info || info.length === 0) {
          that.pageNumber -= 1
        }
        let newFiles = info.map((item) => {
          if (typeof item === 'string') return item
          that.isAnnoDic[`${that.projectName}_${item.fileName}`] = item.isAnno
          return item.fileName
        })
        if (that.files.indexOf(newFiles[0]) === -1) {
          that.$set(that, 'files', [...that.files, ...newFiles])
        }
        console.log(that.files)
        // 如果文件未选中，就选中第一个
        if (that.files[0] && !that.nowFile) {
          that.setNowText(that.files[0])
        }
      })
    },
    lastPage () {
      const that = this
      if (that.pageNumber > 1) {
        that.pageNumber = that.pageNumber - 1
        that.getFiles()
      }
    },
    nextPage () {
      const that = this
      that.pageNumber = that.pageNumber + 1
      that.getFiles()
    },
    goHome: function () {
      this.$router.push({path: '/'})
    },
    save: function () {
      if (window.isLoadingNowText) {
        if (Date.now() - window.isLoadingNowText < 10 * 1000) {
          alert('请等待文件内容加载')
          return false
        } else {
          delete window.isLoadingNowText
        }
      }
      const that = this
      // 保存当前标注
      let annoInfo = {
        projectName: that.projectName,
        fileName: that.nowFile,
        annoDetails: that.ners
      }
      if (that.projectType === '关系标注') {
        annoInfo.relDetails = that.relDetails
      }
      post('/v1/anno/create', annoInfo)
      that.$set(that.nersCache, that.nowFile, [...that.ners])
      return true
    },
    /**
     * 选中目标文件
     * @param name 文件名
     */
    setNowText: function (newFile) {
      const that = this
      window.isLoadingNowText = Date.now()
      that.nowFile = newFile
      that.nowText = that.textDic[newFile]
      const hasCache = !!that.nersCache[newFile]
      that.$set(that, 'ners', that.nersCache[newFile] ? [...that.nersCache[newFile]] : [])
      that.flushWordsType()
      if (that.nowText && that.projectType !== '关系标注') {
        delete window.isLoadingNowText
        return
      } else {
        get(`/v1/anno/query?projectName=${that.projectName}&fileName=${newFile}`, function (info) {
          delete window.isLoadingNowText
          // 如果本地没有缓存，就用线上的标注记录
          if (!hasCache && info.annoDetails) {
            console.log(newFile, that.nowFile)
            if (newFile === that.nowFile) {
              that.$set(that, 'ners', info.annoDetails)
              that.flushWordsType()
            }
            // 更新文件的标注缓存
            that.$set(that.nersCache, newFile, info.annoDetails)
          }
          if (that.projectType === '关系标注' && newFile === that.nowFile) {
            console.log('relDetails', info.relDetails)
            that.$set(that, 'relDetails', info.relDetails || [])
          }
          // 更新文件的文本缓存
          that.$set(that.textDic, newFile, info.fileContent)
          if (newFile === that.nowFile) {
            that.nowText = that.textDic[newFile]
          }
        })
      }
      if (that.files.indexOf(newFile) >= (that.files.length - 1) - 2) {
        // 到倒数第3个文件，就获取下一页
        that.pageNumber = that.pageNumber + 1
        that.getFiles()
      }
      // 列表滚动至选中文件
      let selectFileDom = document.getElementById(newFile)
      let fileListDom = document.getElementById('file-list')
      if (selectFileDom && fileListDom) {
        fileListDom.scrollTop = selectFileDom.offsetTop - 12 - 30 // 保持上方有一个前方文件
      }
    },
    changeIdx: function (d, event) {
      if (event) {
        event.preventDefault() // 防止手机双击放大屏幕
      }
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
        if (!this.nowType) {
          alert('请先选择标签')
          return false
        }
        this.endIdx = idx
        const type = this.nowType
        const start = Math.min(this.startIdx, this.endIdx)
        const end = Math.max(this.startIdx, this.endIdx) + 1
        const name = this.nowText.substring(start, end)
        this.$set(this, 'nowNer', { name, type, start, end, isMove: !config.isDefaultClick })
        return idx
      }
    },
    pointWordByTouch: function (event) {
      event.preventDefault() // 防止触发页面下拉
      let {pageX, pageY} = event.touches[0]
      let dom = document.elementFromPoint(pageX, pageY)
      if (dom && dom.id) {
        this.pointWord(dom.id)
      }
    },
    /**
     * 配置标注类型
     * @param 类型
     */
    setType: function (type, ev) {
      if (!this.nowFile) {
        // 如果没有选中文件，就不允许标注
        return false
      }
      if (this.nerProjectType.indexOf(this.projectType) > -1) {
        this.$set(this, 'nowType', type)
      } else if (this.projectType === '文本分类') {
        let typeIdx = -1
        this.ners.some((ner, idx) => {
          if (ner.type === type) {
            typeIdx = idx
            return ner.type === type
          }
        })
        if (typeIdx === -1) {
          this.ners.push({type})
        } else {
          this.ners.splice(typeIdx, 1)
        }
        this.$set(this, 'nowType', type)
        this.save()
      } else if (this.projectType === '人类反馈强化学习') {
        console.log(this.nowText === type, type)
        this.$set(this, 'nowType', type)
        clearInterval(window.rlhf_inter)
        window.rlhf_inter = setInterval(() => {
          this.$set(this, 'nowType', '')
        }, 200)
      } else {
        console.log(type)
        this.$set(this, 'nowType', type)
      }
    },
    delType: function (type, ev) {
      if (!this.configCanCtlType) return false
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
      that.flushWordsType()
      updateType2Server(that.projectName, that.typeList, that.types)
    },
    checkDelType: function (type, ev) {
      if (!this.configCanCtlType) return false
      ev && ev.stopPropagation()
      const isDel = window.confirm(`确定删除标签【${type}】么？`)
      if (isDel) {
        this.delType(type)
      }
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
      updateType2Server(that.projectName, that.typeList, that.types)
    },
    typeInput: function (ev) {
      this.inputType = ev.target.value
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
    getNerIdxByIdx: function (idx) {
      const ners = this.ners
      for (let i = ners.length - 1; i >= 0; i -= 1) {
        const ner = ners[i]
        if (idx >= ner.start && idx < ner.end) {
          return i
        }
      }
    },
    delIdx: function (idx) {
      const nerIdx = this.getNerIdxByIdx(idx)
      this.del(nerIdx)
    },
    del: function (idx) {
      const ners = this.ners
      ners.splice(idx, 1)
      this.$set(this, 'ners', ners)
      this.save() // 删除时实时保存
    },
    startSelect: function (idx, event) {
      if (this.nerProjectType.indexOf(this.projectType) === -1) return
      if (this.nowType.indexOf('关系-') > -1) {
        if (event.which === 3) return
        if (typeof this.relStartIdx === 'number') {
          console.log(this.relStartIdx, idx)
          this.relDetails.push({
            start: this.relStartIdx,
            end: idx,
            type: this.nowType
          })
          this.$set(this, 'relStartIdx', undefined)
          this.save()
        } else {
          this.$set(this, 'relStartIdx', idx)
        }
        return
      }
      let that = this
      let isNeedDel = false
      if (event.touches) {
        // 手机长按删除
        setTimeout(() => {
          if (window.delMarkIdx === idx) {
            delete window.delMarkIdx
            that.delIdx(idx)
          }
        }, 300)
        window.delMarkIdx = idx
      }
      if (event.which === 3) {
        // 电脑右键删除
        isNeedDel = true
      }
      if (isNeedDel) {
        event.preventDefault()
        // 右键删除对应的图标
        this.delIdx(idx)
        return true
      }
      this.setMode('select')
      this.$set(this, 'nowNer', {})
      this.startIdx = idx
      this.endIdx = idx
      this.pointWord(idx, {isDefaultClick: true})
    },
    stopSelect: function () {
      delete window.delMarkIdx
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
      if (!this.nowType) {
        return false
      }
      const isRepeat = this.checkIsRepeat(this.nowNer)
      if (!isRepeat && this.nowNer.isMove && this.nowNer.name) {
        console.log(this.nowNer)
        delete this.nowNer.isMove
        this.ners.push(this.nowNer)
        this.$set(this, 'ners', this.ners.sort((a, b) => {
          return (a.start - b.start) + (b.end - a.end) * 0.001
        }))
      }
      this.$set(this, 'nowNer', undefined)
      this.flushWordsType()
      this.startIdx = -1
      this.save() // 添加时实时保存
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
      var files = data.files || []
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
      if (!isLocal) {
        // 非单机版，就直接通过url下载
        window.open(`/v1/files/get_anno_json?projectName=${this.projectName}`, '_self')
        return true
      }
      this.nersCache[this.nowFile] = this.ners
      const out = []
      for (const fileName in this.nersCache) {
        const file = fileName
        const text = this.textDic[fileName]
        const entity = JSON.parse(JSON.stringify(this.nersCache[fileName]))
        entity.map((item) => {
          delete item.isSmall
        })
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
    clickColor (type) {
      document.getElementById(type).click()
    },
    // 切换颜色
    changeColor (tarType, ev) {
      const that = this
      console.log(tarType, ev.target.value)
      that.$set(that.types[tarType], 'color', ev.target.value)
      updateType2Server(that.projectName, that.typeList, that.types)
    },
    // 判断标签按钮是否需要被显示成按下
    isTypeSelected (type) {
      if (this.nerProjectType.indexOf(this.projectType) > -1) {
        return this.nowType === type
      } else if (this.projectType === '文本分类') {
        return this.ners.some((ner) => {
          return ner.type === type
        })
      } else {
        return this.nowType === type
      }
    },
    // 请求自动标注接口
    autoAnno () {
      const that = this
      // 获取图片base64
      const img = document.getElementById('anno-img')
      const canvas = document.createElement('canvas')
      const ctx = canvas.getContext('2d')
      // 获取图片原始大小
      const width = img.naturalWidth
      const height = img.naturalHeight
      // 设置canvas的宽高
      canvas.width = width
      canvas.height = height
      // 绘制图片
      ctx.drawImage(img, 0, 0, width, height)
      // 获取base64
      const base64 = canvas.toDataURL('image/png')
      // 去掉前缀
      const base64Data = base64.replace(/^data:image\/\w+;base64,/, '')
      // 请求接口
      const url = 'http://127.0.0.1:5000/detect'
      post(url, {
        projectName: that.projectName,
        'image': base64Data
      }, (info) => {
        // 添加标注
        const _ners = []
        for (let i = 0; i < info.rect_angles.length; i++) {
          const point = info.rect_angles[i]
          const width = info.width
          const height = info.height
          console.log(point)
          _ners.push({
            'type': that.nowType,
            'points': [[point.x / width, point.y / height]]
          })
        }
        that.ners = [..._ners]
        // 保存标注
        that.save()
      })
    }
  },
  watch: {
    ners: function () {
      if (this.nerProjectType.indexOf(this.projectType) > -1) {
        // 给ner加上是否缩小的属性
        let nowSmallAreaEnd
        for (let i = 0; i < this.ners.length; i++) {
          const ner = this.ners[i]
          delete ner.isSmall
          if (nowSmallAreaEnd) {
            if (ner.start <= nowSmallAreaEnd) {
              ner.isSmall = true
            }
          }
          if (!nowSmallAreaEnd) nowSmallAreaEnd = ner.end - 1
          nowSmallAreaEnd = Math.max(nowSmallAreaEnd, ner.end - 1)
        }
      }
    }
  },
  mounted () {
    const that = this
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
      // 除了分类、强化学习，默认选择第一个标签，防止弹出请选择标签的提示
      if (that.typeList && that.typeList[0] && projectType.indexOf('分类') === -1 && projectType.indexOf('强化学习') === -1) that.nowType = that.typeList[0]
      that.getFiles()
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
              // 快捷上一个
              that.changeIdx(-1)
            } else if (type === 'page-down') {
              // 快捷下一个
              that.changeIdx(+1)
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
          // 保存新的快捷键，按Eacape可以起到删除快捷键的作用
          if (key !== 'Escape') that.$set(that.fastKeyType, key, that.nowFocus)
          // 计算新的 类型->键 关系
          const typeKey = {}
          for (const key in that.fastKeyType) {
            const type = that.fastKeyType[key]
            typeKey[type] = key
          }
          that.$set(that, 'fastTypeKey', typeKey)
          localStorage.fastKeyType = JSON.stringify(that.fastKeyType)
          localStorage.fastTypeKey = JSON.stringify(that.fastTypeKey)
        }
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.home,
.now-file {
  position: absolute;
  top: 0;
  left: 0;
  height: 92px;
  padding: 0 10px;
  line-height: 92px;
  font-size: 28px;
  color: #fff;
  cursor: pointer;
  font-weight: 700;
  vertical-align: center;
}
.home {
  background: #1161ca;
  z-index: 2;
}
.now-file {
  left: unset;
  right: 0;
}
.out-title {
  display: inline-block;
  background: #1161ca;
  color: white;
  margin: 0;
  width: 100%;
  height: 92px;
  line-height: 92px;
  font-size: 28px;
  box-sizing: border-box;
  vertical-align: middle;
}
.out-title>.out-title-span {
  position: relative;
  padding: 0 4px;
  display: inline-block;
  background: #1161ca;
}
.layout {
  display: flex;
  flex-direction: column;
}
.container {
  display: flex;
  flex: 1 1;
  flex-direction: row;
  height: calc(100% - 92px);
  background: white;
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
  padding: 0 4px;
  cursor: pointer;
  width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  box-sizing: border-box;
}
.left .file.checked {
  position: relative;
  color: #ccc;
}
.left .file .checked-icon {
  position: absolute;
  right: 2px;
  top: 0;
  bottom: 0;
}
.left .file.selected {
  background: #033271;
  z-index: 5;
}
.left .file-list {
  overflow: auto;
  height: calc(100% - 82px);
}
.left .file-list .process-bar {
  position: absolute;
  top: 0;
  border-top: 2px solid #35e558;
  transition: 0.3s width linear;
}
.left .out-btn,
.left .page-ctl {
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
  user-select: none;
}
.left .page-ctl {
  bottom: 41px;
  cursor: default;
}
.left .page-ctl .page-number {
  min-width: 2em;
}
.left .page-ctl-last:hover,
.left .page-ctl-next:hover,
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
.auto-anno {
  float: right;
  margin-right: 10px;
  cursor: pointer;
  box-sizing: content-box;
  border: 2px solid #03022c;
  text-align: center;
  display: inline-block;
  padding: 0 4px;
  min-width: 100px;
  height: 32px;
  font-size: 18px;
  line-height: 30px;
  border-radius: 4px;
  background: #03022c;
  color: #fff;
  font-weight: 500;
  vertical-align: middle;
  outline: none;
}
button:hover {
  opacity: .7;
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
.type-input-box {
  display: inline-block;
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
  position: relative;
  box-sizing: content-box;
  border: 2px solid #0000;
  text-align: center;
  opacity: .2;
}
.type:hover {
  opacity: .8;
}
@media screen and (max-width: 768px) {
  /* 防止手机点击后持续的hover效果 */
  .type:hover {
    opacity: .2;
  }
}
.type.selected {
  opacity: 1;
}
.result.selected {
  position: relative;
  opacity: 1 !important;
  background: white;
  border: 0;
}
.ner-box {
  position: relative;
  flex: 1;
  padding: 14px;
  margin: 14px;
  border: 1px solid #ccc;
  text-align: left;
  overflow: auto;
  /* font-size: 0; */
}
.ner-box::-webkit-scrollbar {
  /* 隐藏标注区域的滚动条，防止影响到标注定位 */
  width: 0;
}
.ner-box .word {
  display: inline-block;
  position: relative;
  padding-bottom: 15px;
  width: 20px;
  height: 20px;
  line-height: 20px;
  vertical-align: bottom;
  box-sizing: content-box;
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
  overflow: auto;
}
.result {
  position: relative;
  overflow: hidden;
  padding: 0 4px;
  height: 22px;
  text-align: left;
}
.result-type {
  text-align: center;
}
.result-name {
  overflow: hidden;
  height: 100%;
  text-overflow: ellipsis;
  word-break: keep-all;
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
  width: calc(100% - 8px);
}
.result-name-del {
  display: none;
  vertical-align: text-bottom;
  position: absolute;
  right: 0px;
  top: 2px;
}
.result-name-del:hover {
  cursor: pointer;
  opacity: .6;
}
.result-name:hover .result-name-del {
  display: inline-block;
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
}

.color-input {
  width: 0;
  height: 0;
  opacity: 0;
  pointer-events: none;
}
.color-icon {
  display: block;
  float: right;
  margin-top: 6px;
}
.close-icon {
  position: absolute;
  top: -9px;
  right: -9px;
}
@media only screen and (max-width: 800px) {
  .out-title {
    text-align: right !important;
  }
  .now-file  {
    display: none;
  }
}
@media only screen and (max-width: 600px) {
  .out-title {
    font-size: 0;
  }
  .now-file  {
    display: inline-block;
  }
}
@media only screen and (max-width: 800px) {
  .result-box {
    display: none;
  }
  .left {
    display: none;
  }
}
</style>
