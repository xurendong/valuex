<template>
    <div>

        <el-upload class="upload-demo" ref="upload" action="http://127.0.0.1:8080/upload_file" list-type="picture" multiple
            :on-preview="HandlePreview" :on-remove="HandleRemove" :before-remove="BeforeRemove" :on-exceed="HandleExceed"
            :on-success="HandleSuccess" :before-upload="BeforeUpload" :on-change="HandleChange" :on-error="HandleError"
            :on-progress="HandleProgress" :limit="file_limit" :file-list="file_list" :auto-upload="false">
            <el-button slot="trigger" size="small" type="primary">添加文件</el-button>
            <el-button style="margin-left: 10px;" size="small" type="success" @click="SubmitUpload">上传文件</el-button>
            <div slot="tip" class="el-upload__tip">格式限制：xlsx，大小限制：1MB</div>
        </el-upload>

    </div>
</template>

<script>
export default {
    data() {
        return {
            file_limit: 5,
            file_list: []
        };
    },
    methods: {
        SubmitUpload() {
            this.$refs.upload.submit();
        },
        HandleRemove(file, file_list) {
            console.log(file, file_list);
        },
        HandlePreview(file) {
            console.log(file);
        },
        BeforeRemove(file, file_list) {
            return this.$confirm(`移除文件：${file.name}`, '提示', { confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning' });
        },
        HandleExceed(files, file_list) {
            this.$message.warning(`最多上传 5 个文件，本次选择 ${files.length} 个，已经添加 ${file_list.length} 个。`);
        },
        HandleSuccess(response, file, file_list) {
            console.log(response);
            console.log(file.name);
            console.log(file.raw);
            var fileUrl = URL.createObjectURL(file.raw);
            console.log(fileUrl);
        },
        HandleError(err, file, file_list) {
            console.log(err);
        },
        BeforeUpload(file) {
            const file_limit_type = file.type === 'image/jpeg';
            const file_limit_size = file.size / 1024 / 1024 <= 1;
            if (!file_limit_type) {
                this.$message.error(`文件 ${file.name} 格式 异常！`);
            }
            if (!file_limit_size) {
                this.$message.error(`文件 ${file.name} 大小 异常！`);
            }
            return file_limit_type && file_limit_size;
        },
        HandleChange(file, fileList) {
            var suffix = file.name.substring(file.name.lastIndexOf('.') + 1, file.name.length); // 这里的 file 没有 file.type 属性
            const file_limit_type = (suffix === 'jpg' || suffix === 'jpeg' || suffix === 'JPG' || suffix === 'JPEG');
            const file_limit_size = file.size / 1024 / 1024 <= 1;
            if (!file_limit_type) {
                this.$notify.error({ title: '错误', message: `文件 ${file.name} 格式 异常！` });
            }
            if (!file_limit_size) {
                this.$notify.error({ title: '错误', message: `文件 ${file.name} 大小 异常！` });
            }
        },
        HandleProgress(event, file, fileList) {
        }
    }
};
</script>
