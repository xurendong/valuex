<template>
    <div>

        <el-upload class="upload-demo"
            ref="upload"
            action="http://127.0.0.1:8080/"
            :on-preview="handlePreview"
            :on-remove="handleRemove"
            :file-list="fileList"
            :auto-upload="false">
            <el-button slot="trigger" size="small" type="primary">添加文件</el-button>
            <el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload">上传文件</el-button>
            <div slot="tip" class="el-upload__tip">jpg/png ≤ 500kb</div>
        </el-upload>

    </div>
</template>

<script>
export default {
    data() {
        return {
            fileList: []
        };
    },
    methods: {
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
    }
};
</script>
