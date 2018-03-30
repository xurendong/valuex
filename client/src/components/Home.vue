<template>
    <div>

        <div style="margin:10px;">
            <el-upload class="upload-file" ref="upload" :action="upload_url" list-type="picture"
                :on-preview="HandlePreview" :on-remove="HandleRemove" :before-remove="BeforeRemove" :on-exceed="HandleExceed"
                :on-success="HandleSuccess" :before-upload="BeforeUpload" :on-change="HandleChange" :on-error="HandleError"
                :on-progress="HandleProgress" :limit="file_limit" :file-list="file_list" :with-credentials="true" :auto-upload="false">
                <el-button slot="trigger" size="small" type="primary">添加文件</el-button>
                <el-button style="margin-left: 10px;" size="small" type="success" @click="SubmitUpload">上传文件</el-button>
                <div slot="tip" class="el-upload__tip">格式限制：xls xlsx csv，大小限制：5 MB</div>
            </el-upload>
        </div>

    </div>
</template>

<script>
export default {
    data() {
        return {
            upload_url: "http://127.0.0.1:8080/upload_file",
            file_limit: 1,
            size_limit: 5 * 1024 * 1024,
            type_limit: ["xls", "xlsx", "csv"],
            file_list: []
        };
    },
    created() {
    },
    methods: {
        SubmitUpload() {
            this.$refs.upload.submit();
        },
        HandleRemove(file, file_list) {
            console.log(file, file_list);
        },
        HandlePreview(file) {
            // 可以通过 file.response 拿到服务端返回数据
            console.log(file);
        },
        BeforeRemove(file, file_list) {
            return this.$confirm(`移除文件：${file.name}`, '提示', { confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning' });
        },
        HandleExceed(files, file_list) {
            this.$message.warning(`只允许上传 1 个文件，本次选择 ${files.length} 个，已经添加 ${file_list.length} 个。`);
        },
        HandleSuccess(response, file, file_list) {
            console.log(response);
            console.log(file.raw);
            var fileUrl = URL.createObjectURL(file.raw);
            console.log(fileUrl);
            if (response.status === 1) {
                this.$message.info(`文件 ${file.name} 上传成功。${response.message}`);
            } else {
                this.$message.info(`文件 ${file.name} 上传失败！${response.message}`);
            };
        },
        HandleError(error, file, file_list) {
            this.$message.error(`文件 ${file.name} 上传失败！${error}`);
        },
        BeforeUpload(file) {
            return true; // 已在 HandleChange() 中做验证
        },
        GetFileListIndex(file, file_list) {
            for (var i = 0; i < file_list.length; i++) {
                if (file_list[i].name === file.name) {
                    return i;
                };
            };
            return -1;
        },
        HandleChange(file, file_list) {
            var suffix = file.name.substring(file.name.lastIndexOf(".") + 1).toLowerCase(); // 这里的 file 没有 file.type 属性
            const file_limit_type = (this.type_limit.indexOf(suffix) >= 0);
            const file_limit_size = (file.size <= this.size_limit);
            if (!file_limit_type) {
                this.$message.error(`文件 ${file.name} 格式 异常！`);
                var file_index = this.GetFileListIndex(file, file_list);
                if (file_index >= 0) {
                    file_list.splice(file_index, 1);
                };
            };
            if (!file_limit_size) {
                this.$message.error(`文件 ${file.name} 大小 异常！`);
                var file_index = this.GetFileListIndex(file, file_list);
                if (file_index >= 0) {
                    file_list.splice(file_index, 1);
                };
            };
        },
        HandleProgress(event, file, file_list) {
        }
    },
    sockets: {
        connect: function() {
            console.log("socket connect:");
        },
        reconnect: function(times) {
            console.log("socket reconnect: " + times);
        },
        reconnect_attempt: function(times) {
            console.log("socket reconnect_attempt: " + times);
        },
        reconnecting: function(times) {
            console.log("socket reconnecting: " + times);
        },
        reconnect_error: function(error) {
            console.log("socket reconnect_error: " + error);
        },
        reconnect_failed: function(info) {
            console.log("socket reconnect_failed: " + info);
        },
        disconnect: function(info) {
            console.log("socket disconnect: " + info);
        },
        error: function(error) {
            console.log("socket error: " + error);
        },
        my_response: function(data){
            console.log("server data received:");
            console.log(data);
        }
    }
};
</script>
