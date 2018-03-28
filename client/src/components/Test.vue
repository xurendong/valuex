<template>
    <div>
        <p>Test page</p>
        <p>Random number: {{ randomNumber }}</p>
        <el-button type="primary" @click="getRandom">随机</el-button>

        <div style="margin: 20px;">
            <button type="button" class="btn btn-success" @click="changeLocale">中文/English</button>
            <h1>{{$t("message.title")}}</h1>
            <input style="width: 300px;" class="form-control" :placeholder="$t('placeholder.enter')">
            <ul>
                <li v-for="brand in brands" :key="brand.id">{{brand}}</li>
            </ul>
        </div>

    <el-upload class="upload-demo"
        ref="upload"
        action="http://127.0.0.1:8080/upload_file"
        :on-preview="handlePreview"
        :on-remove="handleRemove"
        :file-list="fileList"
        :auto-upload="false">
        <el-button slot="trigger" size="small" type="primary">添加文件</el-button>
        <el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload">上传文件</el-button>
        <div slot="tip" class="el-upload__tip">jpg/png ≤ 500kb</div>
    </el-upload>

    <!-- 导入 -->
<!-- 
    <el-dialog title="上传文件" :visible.sync="dialogImportVisible" :modal-append-to-body="false" :close-on-click-modal="false" class="dialog-import">
      <div :class="{'import-content': importFlag === 1, 'hide-dialog': importFlag !== 1}">
        <el-upload class="upload-demo"
        :action="uploadUrl"
        :name ="name"
        :headers="importHeaders"
        :on-preview="handlePreview"
        :on-remove="handleRemove"
        :before-upload="beforeUpload"
        :on-error="uploadFail"
        :on-success="uploadSuccess"
        :file-list="fileList"
        :with-credentials="withCredentials">
          <el-button size="small" type="primary" :disabled="processing">{{ uploadTip }}</el-button>
          <div slot="tip" class="el-upload__tip">只能上传excel文件</div>
        </el-upload>
        <div class="download-template">
          <a class="btn-download" @click="download">
            <i class="icon-download"></i>下载模板</a>
        </div>
      </div>
      <div :class="{'import-failure': importFlag === 2, 'hide-dialog': importFlag !== 2}" >
        <div class="failure-tips">
          <i class="el-icon-warning"></i>导入失败</div>
        <div class="failure-reason">
          <h4>失败原因</h4>
          <ul>
            <li v-for="(error,index) in errorResults" :key="index">第{{ error.rowIdx + 1 }}行，错误：{{ error.column }},{{ error.value }},{{ error.errorInfo }}</li>
          </ul>
        </div>
      </div>
    </el-dialog>
-->

    </div>
</template>

<script>
import axios from "axios";
export default {
    data() {
        return {
            randomNumber: 0,
            brands: [
                this.$t("brands.nike"),
                this.$t("brands.adi"),
                this.$t("brands.nb"),
                this.$t("brands.ln")
            ],
            // importHeaders:{
            //   enctype:'multipart/form-data',
            //   cityCode:''
            // },
            // uploadUrl: 'www.baidu.com',
            // name: 'import',
            // fileList: [],
            // withCredentials: true,
            // processing: false,
            // uploadTip:'点击上传',
            // importFlag:1,
            // dialogImportVisible:false,
            // errorResults:[]
            fileList: []
        };
    },
    methods: {
        getRandomFromServer() {
            const path = `http://127.0.0.1:8080/random`;
            axios
                .get(path)
                .then(response => {
                    this.randomNumber = response.data.randomNumber;
                })
                .catch(error => {
                    console.log(error);
                });
        },
        getRandom() {
            this.getRandomFromServer();
        },
        changeLocale() {
            this.$confirm(this.$t("layer.toggle"), this.$t("layer.tips"), {
                confirmButtonText: this.$t("button.ok"),
                cancelButtonText: this.$t("button.cancel"),
                type: "warning"
            })
                .then(() => {
                    let locale = this.$i18n.locale;
                    locale === "zh"
                        ? (this.$i18n.locale = "en")
                        : (this.$i18n.locale = "zh");
                    this.brands = [
                        this.$t("brands.nike"),
                        this.$t("brands.adi"),
                        this.$t("brands.nb"),
                        this.$t("brands.ln")
                    ];
                })
                .catch(() => {
                    this.$message({
                        type: "info"
                    });
                });
        },
        submitUpload() {
            this.$refs.upload.submit();
        },
        handleRemove(file, fileList) {
            console.log(file, fileList);
        },
        handlePreview(file) {
            console.log(file);
        }
        // importData() {
        //   this.importFlag = 1
        //   this.fileList = []
        //   this.uploadTip = '点击上传'
        //   this.processing = false
        //   this.dialogImportVisible = true
        // },
        // uploadUrl() {
        //   this.uploadUrl = 'www.baidu.com' //后台接口config.admin_url+'rest/schedule/import/'
        // },
        // handlePreview(file) {
        //   //可以通过 file.response 拿到服务端返回数据
        // },
        // handleRemove(file, fileList) {
        //   //文件移除
        // },
        // beforeUpload(file){
        //   //上传前配置
        //   this.importHeaders.cityCode='上海'//可以配置请求头
        //   let excelfileExtend = ".xls,.xlsx,.doc,.docx"//设置文件格式
        //   let fileExtend = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
        //   if (excelfileExtend.indexOf(fileExtend) <= -1) {
        //      this.$message.error('文件格式错误')
        //      return false
        //   }
        //   const isLt2M = file.size / 1024 / 1024 < 10
        //   if (!isLt2M) {
        //     this.$message.error('上传模板大小不能超过 10MB!')
        //     return false
        //   }
        //   this.uploadTip = '正在处理中...'
        //   this.processing = true
        // },
        // //上传错误
        // uploadFail(err, file, fileList) {
        //   this.uploadTip = '上传失败，点击上传'
        //   this.processing = false
        //   this.$message.error(err)
        // },
        // //上传成功
        // uploadSuccess(response, file, fileList) {
        //   this.uploadTip = '点击上传'
        //   this.processing = false
        //   if (response.status === -1) {
        //     this.errorResults = response.data
        //     if (this.errorResults) {
        //       this.importFlag = 2
        //     } else {
        //       this.dialogImportVisible = false
        //       this.$message.error(response.errorMsg)
        //     }
        //   } else {
        //     this.importFlag = 3
        //     this.dialogImportVisible = false
        //     this.$message.info('导入成功')
        //     this.doSearch()
        //   }
        // }
    },
    created() {
        this.getRandom();
    }
};
</script>
