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
        <div style="margin:10px;">
            <el-button type="primary" :disabled="button_make_report_disabled" @click="MakeReport">生成报告</el-button>
            <el-button style="margin-left: 10px;" size="small" type="success" :disabled="button_view_report_disabled" @click="ViewReport">浏览报告</el-button>
        </div>

    </div>
</template>

<script>
import axios from "axios";
export default {
    data() {
        return {
            upload_url: process.env.SITE_URL + "/upload_file",
            file_limit: 1,
            size_limit: 5 * 1024 * 1024,
            type_limit: ["xls", "xlsx", "csv"],
            file_list: [],
            button_make_report_disabled: true, // 禁用
            button_view_report_disabled: true // 禁用
        };
    },
    created() {
    },
    methods: {
        MakeReport() {
            const path = process.env.SITE_URL + "/make_report";
            axios.get(path
            ).then(response => {
                if (response.data.status === 1) {
                    this.$message.info(`报告生成成功。${response.data.message}`);
                    this.button_view_report_disabled = false; // 可用
                } else {
                    this.$message.info(`报告生成失败！${response.data.message}`);
                    this.button_view_report_disabled = true; // 禁用
                };
            }).catch(error => {
                console.log(error);
            });
        },
        ViewReport() {
            const path = process.env.SITE_URL + "/check_report";
            axios.get(path
            ).then(response => {
                if (response.data.status === 1) {
                    this.$message.info(`报告查验成功。${response.data.message}`);
                    window.open("/view_report");
                } else {
                    this.$message.info(`报告查验失败！${response.data.message}`);
                };
            }).catch(error => {
                console.log(error);
            });
        },
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
                this.button_make_report_disabled = false; // 可用
                this.button_view_report_disabled = true; // 禁用
            } else {
                this.$message.info(`文件 ${file.name} 上传失败！${response.message}`);
                this.button_make_report_disabled = true; // 禁用
                this.button_view_report_disabled = true; // 禁用
            };
        },
        HandleError(error, file, file_list) {
            this.$message.error(`文件 ${file.name} 上传失败！${error}`);
            this.button_make_report_disabled = true; // 禁用
            this.button_view_report_disabled = true; // 禁用
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
