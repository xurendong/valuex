/*
* Copyright (c) 2018-2018 the ValueX authors
* All rights reserved.
*
* The project sponsor and lead author is Xu Rendong.
* E-mail: xrd@ustc.edu, QQ: 277195007, WeChat: ustc_xrd
* You can get more information at https://xurendong.github.io
* For names of other contributors see the contributors file.
*
* Commercial use of this code in source and binary forms is
* governed by a LGPL v3 license. You may get a copy from the
* root directory. Or else you should get a specific written 
* permission from the project author.
*
* Individual and educational use of this code in source and
* binary forms is governed by a 3-clause BSD license. You may
* get a copy from the root directory. Certainly welcome you
* to contribute code of all sorts.
*
* Be sure to retain the above copyright notice and conditions.
*/

import Vue from "vue";
import App from "./App";
import router from "./router";

import ElementUI from "element-ui";
import "element-ui/lib/theme-chalk/index.css";

import VueI18n from "vue-i18n";
import enLocale from "element-ui/lib/locale/lang/en";
import zhLocale from "element-ui/lib/locale/lang/zh-CN";

Vue.use(VueI18n);

const i18n = new VueI18n({
    locale: "zh",
    messages: {
        // 合并 自定义 与 element-ui 的翻译
        en: Object.assign(require("../static/js/zh.js"), enLocale),
        zh: Object.assign(require("../static/js/en.js"), zhLocale)
    }
});

Vue.use(ElementUI, { i18n: (key, value) => i18n.t(key, value), size: "small" });

Vue.config.productionTip = false;

new Vue({
    el: "#app",
    i18n,
    router,
    components: { App },
    template: "<App/>"
});
