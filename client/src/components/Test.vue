<template>
    <div>
        <p>Random number: {{random_number}}</p>
        <el-button type="primary" @click="getRandom">随机</el-button>

        <div style="margin: 20px;">
            <button type="button" class="btn btn-success" @click="changeLocale">中文/English</button>
            <h1>{{$t("message.title")}}</h1>
            <input style="width: 300px;" class="form-control" :placeholder="$t('placeholder.enter')">
            <ul>
                <li v-for="brand in brands" :key="brand.id">{{brand}}</li>
            </ul>
        </div>

        <div style="margin:10px;">
            <el-upload class="upload-demo" ref="upload" action="http://127.0.0.1:8080/upload_file" list-type="picture" multiple
                :on-preview="HandlePreview" :on-remove="HandleRemove" :before-remove="BeforeRemove" :on-exceed="HandleExceed"
                :on-success="HandleSuccess" :before-upload="BeforeUpload" :on-change="HandleChange" :on-error="HandleError"
                :on-progress="HandleProgress" :limit="file_limit" :file-list="file_list" :with-credentials="credentials" :auto-upload="false">
                <el-button slot="trigger" size="small" type="primary">添加文件</el-button>
                <el-button style="margin-left: 10px;" size="small" type="success" @click="SubmitUpload">上传文件</el-button>
                <div slot="tip" class="el-upload__tip">格式限制：xls xlsx csv，大小限制：5 MB</div>
            </el-upload>
        </div>

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

        <div style="margin:10px;">
            <el-button size="small" type="primary" @click="TestSocketIO">SocketIO</el-button>
            <el-button style="margin-left: 10px;" size="small" type="primary" @click="TestSocketIO_Broadcast">Broadcast</el-button>
        </div>

    </div>
</template>

<script>
import axios from "axios";
export default {
    data() {
        return {
            random_number: 0,
            brands: [
                this.$t("brands.nike"),
                this.$t("brands.adi"),
                this.$t("brands.nb"),
                this.$t("brands.ln")
            ],
            file_limit: 3,
            size_limit: 5 * 1024 * 1024,
            type_limit: ["xls", "xlsx", "csv"],
            file_list: [],
            credentials: false, // 如果 true 则报：Credential is not supported if the CORS header ‘Access-Control-Allow-Origin’ is ‘*’
            placeholder_text: "输入任务编号",
            task_id_input: "",
            task_dict: {},
            socket_id: "",
            socket_connect: false
        };
    },
    created() {
    },
    methods: {
        getRandomFromServer() {
            const path = `http://127.0.0.1:8080/random`;
            axios.get(path
            ).then(response => {
                this.random_number = response.data.random_number;
            }).catch(error => {
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
            }).then(() => {
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
            }).catch(() => {
                this.$message({
                    type: "info"
                });
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
            this.$message.warning(`只允许上传 3 个文件，本次选择 ${files.length} 个，已经添加 ${file_list.length} 个。`);
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
        },
        TestSocketIO() {
            this.$socket.emit("my_event", { msg: "Hello World" });
        },
        TestSocketIO_Broadcast() {
            this.$socket.emit("my_event", { msg: "Hello World - Broadcast" });
        }
    },
    sockets: {
        connect: function() {
            this.socket_id = this.$socket.id;
            this.socket_connect = true;
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
