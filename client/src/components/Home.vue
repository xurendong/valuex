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

        <div style="margin:10px;">
            <el-input style="width: 300px;" :placeholder="placeholder_text" v-model="task_id_input"></el-input>
        </div>
        <div style="margin:10px;">
            <el-button size="small" type="primary" @click="GetAllTasks">列表</el-button>
            <el-button style="margin-left: 10px;" size="small" type="primary" @click="AddOneTask">增加</el-button>
            <el-button style="margin-left: 10px;" size="small" type="primary" @click="GetOneTask">单个</el-button>
            <el-button style="margin-left: 10px;" size="small" type="primary" @click="DelOneTask">删除</el-button>
            <el-button style="margin-left: 10px;" size="small" type="primary" @click="UpdateOneTask">更新</el-button>
        </div>
        <div style="margin:10px;">
            <ul>
                <li v-for="(value, key) in task_dict" :key="value.id">{{key}}: {{value.task}}</li>
            </ul>
        </div>

    </div>
</template>

<script>
export default {
    data() {
        return {
            file_limit: 5,
            file_list: [],
            placeholder_text: "输入任务编号",
            task_id_input: '',
            task_dict: {}
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
        },
        GetAllTasks() {
            this.$http.get("http://127.0.0.1:8080/restful", {
                // 设置参数
            }).then((response) => {
                this.$message.success("列表 task 成功。");
                console.log(response.body);
                this.task_dict = response.body;
            }, (response) => {
                this.$message.error("列表 task 失败！");
                console.log(response);
            }).catch(function(response) {
                this.$message.error("列表 task 异常！");
                console.log(response);
            });
        },
        AddOneTask() {
            this.$http.post("http://127.0.0.1:8080/restful?workname=something_add", {
                // 设置参数
            }).then((response) => {
                this.$message.success("增加 task 成功。");
                console.log(response.body);
                this.GetAllTasks();
            }, (response) => {
                this.$message.error("增加 task 失败！");
                console.log(response);
            }).catch(function(response) {
                this.$message.error("增加 task 异常！");
                console.log(response);
            });
        },
        GetOneTask() {
            this.$http.get(`http://127.0.0.1:8080/restful/${this.task_id_input}`, {
                // 设置参数
            }).then((response) => {
                this.$message.success("单个 task 成功。");
                console.log(response.body);
                this.$notify.info({ title: '任务', message: `${response.body.task}` });
            }, (response) => {
                this.$message.error("单个 task 失败！");
                console.log(response);
            }).catch(function(response) {
                this.$message.error("单个 task 异常！");
                console.log(response);
            });
        },
        DelOneTask() {
            this.$http.delete(`http://127.0.0.1:8080/restful/${this.task_id_input}`, {
                // 设置参数
            }).then((response) => {
                this.$message.success("删除 task 成功。");
                console.log(response.body);
                this.GetAllTasks();
            }, (response) => {
                this.$message.error("删除 task 失败！");
                console.log(response);
            }).catch(function(response) {
                this.$message.error("删除 task 异常！");
                console.log(response);
            });
        },
        UpdateOneTask() {
            this.$http.put(`http://127.0.0.1:8080/restful/${this.task_id_input}?workname=something_update`, {
                // 设置参数
            }).then((response) => {
                this.$message.success("更新 task 成功。");
                console.log(response.body);
                this.GetAllTasks();
            }, (response) => {
                this.$message.error("更新 task 失败！");
                console.log(response);
            }).catch(function(response) {
                this.$message.error("更新 task 异常！");
                console.log(response);
            });
        }
    }
};
</script>
