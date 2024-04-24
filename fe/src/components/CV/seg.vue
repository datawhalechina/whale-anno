<template>
  <div class="anno-img-box">
    <div class="seg-box">
      <img class="anno-img" id="anno-img" @click="addSeg($event)" :src="`data:image/jpeg;base64,${fileContent}`" @dragstart="$event.preventDefault()" @contextmenu="$event.preventDefault()">
      <div v-for="annoDetail in annoDetails" :seg="annoDetail" :key="`${annoDetail.segs[0][0]}_${annoDetail.segs[0][1]}`" :style="{
        left: annoDetail.segs[0][0]*100 + '%',
        top: annoDetail.segs[0][1]*100 + '%',
        backgroundColor: types[annoDetail.type]?types[annoDetail.type].color:'#f00',
      }" class="seg" @contextmenu="$event.preventDefault();delSeg(annoDetail, true)" @touchstart="$event.preventDefault();delSeg(annoDetail, false)" @mouseover="overSeg($event, annoDetail)"></div>
    </div>
  </div>
</template>

<script>
// import npyjs from 'npyjs'
import { InferenceSession, Tensor } from 'onnxruntime-web'

const ort = require('onnxruntime-web')

console.log(ort)
// console.log(npyjs)

// const IMAGE_PATH = '/assets/data/dogs.jpg'
const IMAGE_EMBEDDING = '/assets/data/dogs_embedding.npy'
// const MODEL_DIR = '/assets/data/sam_onnx_quantized_example.onnx'
const MODEL_DIR = './sam_onnx_quantized_example.onnx'
let model = null
async function getModel () {
  console.log(InferenceSession, MODEL_DIR)
  model = await InferenceSession.create(MODEL_DIR)
  console.log('model', model)
  // go()
}
getModel()

// Use a Canvas element to produce an image from ImageData
function imageDataToImage (imageData) {
  const canvas = imageDataToCanvas(imageData)
  const image = new Image()
  image.src = canvas.toDataURL()
  return image
}

// Convert the onnx model mask prediction to ImageData
function arrayToImageData (input, width, height) {
  const [r, g, b, a] = [0, 114, 189, 255] // the masks's blue color
  const arr = new Uint8ClampedArray(4 * width * height).fill(0)
  for (let i = 0; i < input.length; i++) {
    // Threshold the onnx model mask prediction at 0.0
    // This is equivalent to thresholding the mask using predictor.model.mask_threshold
    // in python
    if (input[i] > 0.0) {
      arr[4 * i + 0] = r
      arr[4 * i + 1] = g
      arr[4 * i + 2] = b
      arr[4 * i + 3] = a
    }
  }
  return new ImageData(arr, height, width)
}

// Canvas elements can be created from ImageData
function imageDataToCanvas (imageData) {
  const canvas = document.createElement('canvas')
  const ctx = canvas.getContext('2d')
  canvas.width = imageData.width
  canvas.height = imageData.height
  ctx.putImageData(imageData, 0, 0)
  return canvas
}

// Convert the onnx model mask output to an HTMLImageElement
export function onnxMaskToImage (input, width, height) {
  return imageDataToImage(arrayToImageData(input, width, height))
}
// async function go () {
//   let n = 0
//   const pointCoords = new Float32Array(2 * (n + 1))
//   const pointLabels = new Float32Array(n + 1)

//   // Add in the extra point/label when only clicks and no box
//   // The extra point is at (0, 0) with label -1
//   pointCoords[2 * n] = 0.0
//   pointCoords[2 * n + 1] = 0.0
//   pointLabels[n] = -1.0

//   const feeds = {
//     image_embeddings: new Tensor('float32', [
//       256,
//       64,
//       64
//     ]),
//     point_coords: new Tensor('float32', pointCoords, [1, n + 1, 2]),
//     point_labels: new Tensor('float32', pointLabels, [1, n + 1]),
//     orig_im_size: new Tensor('float32', [
//       256,
//       256
//     ]),
//     mask_input: new Tensor(
//       'float32',
//       new Float32Array(256 * 256),
//       [1, 1, 256, 256]
//     ),
//     has_mask_input: new Tensor('float32', [0])
//   }
//   const results = await model.run(feeds)
//   const output = results[model.outputNames[0]]
//   // The predicted mask returned from the ONNX model is an array which is
//   // rendered as an HTML image using onnxMaskToImage() from maskUtils.tsx.
//   let img = onnxMaskToImage(output.data, output.dims[2], output.dims[3])
//   console.log(img)
// }

// Decode a Numpy file into a tensor.
const loadNpyTensor = async (tensorFile, dType) => {
  // let npLoader = new npyjs()
  // const npArray = await npLoader.load(tensorFile)
  // const tensor = new ort.Tensor(dType, npArray.data, npArray.shape)
  // return tensor
}
// Load the Segment Anything pre-computed embedding
Promise.resolve(loadNpyTensor(IMAGE_EMBEDDING, 'float32')).then(
  (embedding) => console.log(embedding)
)

// Run the ONNX model every time clicks has changed
const modelData = ({ clicks, tensor, modelScale }) => {
  const imageEmbedding = tensor
  let pointCoords
  let pointLabels
  let pointCoordsTensor
  let pointLabelsTensor

  // Check there are input click prompts
  if (clicks) {
    let n = clicks.length

    // If there is no box input, a single padding point with
    // label -1 and coordinates (0.0, 0.0) should be concatenated
    // so initialize the array to support (n + 1) points.
    pointCoords = new Float32Array(2 * (n + 1))
    pointLabels = new Float32Array(n + 1)

    // Add clicks and scale to what SAM expects
    for (let i = 0; i < n; i++) {
      pointCoords[2 * i] = clicks[i].x * modelScale.samScale
      pointCoords[2 * i + 1] = clicks[i].y * modelScale.samScale
      pointLabels[i] = clicks[i].clickType
    }

    // Add in the extra point/label when only clicks and no box
    // The extra point is at (0, 0) with label -1
    pointCoords[2 * n] = 0.0
    pointCoords[2 * n + 1] = 0.0
    pointLabels[n] = -1.0

    // Create the tensor
    pointCoordsTensor = new Tensor('float32', pointCoords, [1, n + 1, 2])
    pointLabelsTensor = new Tensor('float32', pointLabels, [1, n + 1])
  }
  const imageSizeTensor = new Tensor('float32', [
    modelScale.height,
    modelScale.width
  ])

  if (pointCoordsTensor === undefined || pointLabelsTensor === undefined) {
    return
  }

  // There is no previous mask, so default to an empty tensor
  const maskInput = new Tensor(
    'float32',
    new Float32Array(256 * 256),
    [1, 1, 256, 256]
  )
  // There is no previous mask, so default to 0
  const hasMaskInput = new Tensor('float32', [0])

  return {
    image_embeddings: imageEmbedding,
    point_coords: pointCoordsTensor,
    point_labels: pointLabelsTensor,
    orig_im_size: imageSizeTensor,
    mask_input: maskInput,
    has_mask_input: hasMaskInput
  }
}
console.log(modelData)

// const runONNX = async () => {
//   try {
//     if (
//       model === null ||
//       clicks === null ||
//       tensor === null ||
//       modelScale === null
//     ) {
//       return
//     } else {
//       // Preapre the model input in the correct format for SAM.
//       // The modelData function is from onnxModelAPI.tsx.
//       const feeds = modelData({
//         clicks,
//         tensor,
//         modelScale,
//       })
//       if (feeds === undefined) return
//       // Run the SAM ONNX model with the feeds returned from modelData()
//       const results = await model.run(feeds)
//       const output = results[model.outputNames[0]]
//       // The predicted mask returned from the ONNX model is an array which is
//       // rendered as an HTML image using onnxMaskToImage() from maskUtils.tsx.
//       setMaskImg(onnxMaskToImage(output.data, output.dims[2], output.dims[3]))
//     }
//   } catch (e) {
//     console.log(e)
//   }
// }

export default ({
  name: 'CVSeg',
  props: {
    fileContent: {
      type: String,
      default: '',
      required: true
    },
    annoDetails: {
      type: Array,
      default: () => [],
      required: true
    },
    nowType: {
      type: String,
      default: '1234',
      required: true
    },
    types: {
      type: Object,
      default: () => {},
      required: true
    },
    save: {
      type: Function,
      required: true
    }
  },
  data () {
    return {
      segs: [],
      width: 0,
      height: 0
    }
  },
  methods: {
    log (...args) {
      console.log(args)
    },
    addSeg (ev) {
      ev.preventDefault()
      if (!this.nowType) {
        alert('请先选择标注类型')
        return
      }
      const tar = ev.target
      const newSeg = [ev.offsetX / tar.offsetWidth, ev.offsetY / tar.offsetHeight]
      // this.segs.push(newSeg)
      // console.log(this.segs)
      this.annoDetails.push({
        segs: [newSeg],
        type: this.nowType
      })
      this.save()
      return false
    },
    delSeg (annoDetail, isForce) {
      if (!isForce) {
        // 非强制删除，就判定下当前类型是否一致，不一致就不删除
        if (this.nowType !== annoDetail.type) {
          return
        }
      }
      const idx = this.annoDetails.indexOf(annoDetail)
      console.log(annoDetail, this.segs)
      this.annoDetails.splice(idx, 1)
      this.save()
    },
    overSeg (ev, seg) {
      if (ev.which === 3) {
        this.delSeg(seg)
      }
    }
  },
  watch: {
    annoDetails: {
      handler (val) {
        // const annoImg = document.getElementById('anno-img')
        // annoImg.src = val
        // console.log(annoImg.width)
        // this.width = annoImg.width
        // this.height = annoImg.height
        console.log(val)
      },
      deep: true
    }
  }
})
</script>

<style>
.anno-img-box {
  position: relative;
  display: flex;
  height: 100%;
  align-content: center;
  justify-content: center;
}
.anno-img {
  width: 100%;
  user-select: none;
}
.seg-box {
  width: 400px;
  position: absolute;
  font-size: 0;
}
.seg {
  position: absolute;
  width: 8px;
  height: 8px;
  transform: translateX(-50%) translateY(-50%);
  border-radius: 50%;
  background-color: #f00;
}
.seg:hover {
  width: 16px;
  height: 16px;
}
</style>
