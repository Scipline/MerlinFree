// ==UserScript==
// @name        Merlin Enhance Plugin
// @namespace   https://github.com/Scipline
// @version      2.6.0
// @description  由于涉及跨域请求，提示'一个用户脚本试图访问跨源资源',需要总是允许请求操作/Due to a cross-domain request, a message is displayed stating that 'a user script is attempting to access a cross-origin resource'. It is necessary to always allow the request operation.
// @author       Scipline
// @license      GPL version 3
// @match        https://www.getmerlin.in/*
// @match        https://app.getmerlin.in/*
// @icon         data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABmJLR0QA/wD/AP+gvaeTAAAEbklEQVRYhb2XW4hVZRTHf/vMMZvRoDJFMy81FKWYdIMgMnoYexDS6CmNpBSqhygvUZBhEklE00QWIWYwJfbgQ4hElBVlJdHlsYKQvA2OjgbRnLNv3/7W6uHbt7PPeMb7hu98Z5+9Of/fuuy11vYAoiia53ne26D3ApdzEQ6xigkVG0oYh7LP+qyZMf+KPzwnzq9A98UQzgESB5CEggkFE2pgAu+OmrP84ooDaPqpxU/dnmcHvDiO/EsBYI1iQiEJs10wofq1SyEOoAooqGq6gyo9tUshDqCiqOCWZkBKR4CmH9D0g3MWDcKQRqNZElYnXoLpCPDQ8qdZvHQlBw8dPWvx4eMjLHl4NYuXrUSsFBC5uIPpCHD7rfM5MXKKFavXnhXE8PERlq9aw5GhYyxcMA9VDxVFbDtER4DXNq5j6ZI+Rk7+wyNPPMeBvw+PL37iJCtWreXo0DD33XMXA5s3oDYTV9SCpOJiwYvjSDv9obXC+pc2s+fzb5g2dQp7dw8yaVLPmPcaY3hg2eMcGTrG/Yvu5r3+TXR5dZJISSJxhShKH8HIFaUzegpqta70W0fW9A53T82r4eFKsFhFEk09kXrDOm90BLBWeHHjG+z+bC9Trr6Swa1vntZ6gAkTJrBz+wCzrpvB19/t58lnXyYMDJI4UUlFMwgZLwc2vPoWn+75kqnXXMXODwe4sXcuAM2mzzPrN/HVtz9irbDp9XfYPrgLgBnTp7FjWz8zr53Ovv0/8/zGzYUXLKknUgijnXOgb+lKms0mH2/rp/f6OfnvBw8P0ffgY0yceBlzZs3krwMHuW3hfHZ9tCW/58ihYR59ah1RFPHFjk+wsea5kESuMcW+7QzQaDQBmDx5Utu19z/YyZatg8SxYe7smbzb/wo339QLOOuSSPnvX584TOiu9+TC5YSMGuMAjHeMjjY4PnKKG+bOpqvLRVMFkliwkZLEqcUV65NIiH0hasj5AVQPVZyrYylcXoWJXDeMGw7gwjUjdS3XGkl3t8QoNsnOwSZahCIW6hdEOxOPK8u0LimLp944bwCVkuVjiLaIx64KFpXwPAHEVoTiyl655qah0mwYnWMIVMlj2xLjknBSCYMJBRNIeSg9Bw8o2LSuS+KSSpLTuD0uwmICJ16GyEDOCECFtnJaQJQ8MQaEE1fiQDEty0GcFiAbGETI+3nW1dyeWl8NQ2ll4sYXjO+KT+ENB1IXm06pqYurM1sxyWhLV8s9kLSGQZLU8tTdcQYQZOfSEpK6CQv1fHTOBkihELe09PMCoDUf3KOmpZhrq+UViHoSSoDSXXhAi9E580Tau/N+XgqDLYEkUfbqle5ZCMqifguEXzeh/IDSlz1e7WFozwMthSGLfV7hUoD87SfQdst9wfhK5Ov33vDvo/PE4xfQHrK5XWmbXtuTsXC5LbfZsbwQViB8xQTix5He6QEc+m30Fs+zA6osUqWbShhaJ1qX9UlW3WJNu13aakPFRJV3wKBIShNIEPm6L4l1zQs/Lfjzf2TQwc8hAO5kAAAAAElFTkSuQmCC
// @grant        GM_xmlhttpRequest
// @grant        GM_setValue
// @grant        GM_getValue
// @run-at      document-end
// ==/UserScript==

function get_token() {
    /**
   * This function is used to get the token from the authorization API.
   * @returns {Promise} A promise that resolves with the token if the HTTP request is successful, otherwise it rejects with an error.
   */
    return new Promise((resolve, reject) => {
        GM_xmlhttpRequest({
            method: 'POST',
            url: 'http://8.130.132.80:4000/api/authorization',
            headers: {
                'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36)',
            },
            onload: function (response) {
                var result = JSON.parse(response.responseText)
                resolve(result.token)
            },
            onerror: function (response) {
                reject(new Error('HTTP request failed with status ' + response.status))
            },
        })
    })
}

function get_and_delete_chat_history(accessToken) {
    /**
   * This function is used to get and delete the chat history.
   * @param {string} accessToken - The access token used for authorization.
   * @returns {Promise} A promise that resolves with the list of chat IDs if the HTTP request is successful, otherwise it rejects with an error.
   */
    return new Promise((resolve, reject) => {
        // 获取历史记录
        GM_xmlhttpRequest({
            method: 'POST',
            url: 'https://merlin-uam-yak3s7dv3a-ue.a.run.app/user/getPaginatedUserChatHistory?customJWT=true',
            headers: {
                'authority': 'merlin-uam-yak3s7dv3a-ue.a.run.app',
                'accept': '*/*',
                'accept-language': 'zh-CN,zh;q=0.9',
                'authorization': 'Bearer ' + accessToken,
                'content-type': 'application/json',
            },
            data: JSON.stringify({
                ENTRY_PER_PAGE: 30,
                page: 1,
            }),
            onload: function (response) {
                var response_dict = JSON.parse(response.responseText)
                var id_list = response_dict.data.history.map((history) => history.id)

                if (!id_list.length) {
                    reject(new Error('获取历史记录失败或历史记录为空'))
                    return
                }

                // 删除历史记录
                var deletePromises = id_list.map((chat_id) => {
                    return new Promise((resolve, reject) => {
                        GM_xmlhttpRequest({
                            method: 'GET',
                            url: `https://us-central1-foyer-work.cloudfunctions.net/deleteUserChatHistory?token=${accessToken}&chatId=${chat_id}&customJWT=true`,
                            headers: {
                                'authority': 'us-central1-foyer-work.cloudfunctions.net',
                                'accept': '*/*',
                                'accept-language': 'zh-CN,zh;q=0.9',
                                'content-type': 'application/json',
                            },
                            onload: function (response) {
                                var response_data = JSON.parse(response.responseText).data
                                console.log(`Chat_id=${chat_id}: ${response_data.message}`)
                                resolve()
                            },
                            onerror: function (response) {
                                reject(new Error('删除历史记录失败，AccessToken有误'))
                            },
                        })
                    })
                })

                Promise.all(deletePromises)
                    .then(() => resolve(id_list))
                    .catch((err) => reject(err))
            },
            onerror: function (response) {
                reject(new Error('获取历史记录失败，AccessToken有误'))
            },
        })
    })
}
window.onload = function () {
    ;(function () {
        /**
   * This function is executed when the window is loaded. It creates a new button and inserts it into the target element.
   */
        'use strict'



        // Create an observer instance linked to the callback function.
        const observer = new MutationObserver(function(mutationsList, observer) {

            // 查找目标元素X
            const targetElement = document.querySelector('span.flex.gap-6')
            if (targetElement) {
                // 创建新的按钮元素

                const newButton1 = document.createElement('button')
                newButton1.type = 'button'
                newButton1.className = 'cursor-pointer'
                newButton1.innerHTML =
                    '<div class="text-lg font-medium bg-cta-btn py-2 px-4 rounded flex gap-2 "><span class="">Clear</span></div>'

                // 绑定事件处理函数
                newButton1.addEventListener('click', function () {
                    // 从存储中获取 accessToken
                    const accessToken = GM_getValue('accessToken')
                    get_and_delete_chat_history(accessToken)
                })

                // 将新的按钮作为第一个子元素插入到目标元素中
                targetElement.insertBefore(newButton1, targetElement.firstChild)
                const newButton = document.createElement('button')
                newButton.type = 'button'
                newButton.className = 'cursor-pointer'
                newButton.innerHTML =
                    '<div class="text-lg font-medium bg-cta-btn py-2 px-4 rounded flex gap-2 "><span class="">Reset</span></div>'

                // 绑定事件处理函数
                newButton.addEventListener('click', function () {
                    get_token().then((accessToken) => {
                        // const Pd = 'camppjleccjaphfdbohjdohecfnoikec'
                        const data = {
                            accessToken: accessToken,
                            refreshToken:
                            'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0',
                        }
                        //MerlinChat插件
                        chrome.runtime.sendMessage("camppjleccjaphfdbohjdohecfnoikec", {
                            from: 'MERLIN_APP',
                            action: 'SIGNIN',
                            payload: {
                                session: data,
                                closeTab: false,
                            },
                        })
                        //新增Merlin旗下的PixPlain插件
                        chrome.runtime.sendMessage("nfddopbgedlmbjbnpomhcamablpkbpnb", {
                            from: 'MERLIN_APP',
                            action: 'SIGNIN',
                            payload: {
                                session: data,
                                closeTab: false,
                            },
                        })
                        // 将获取到的 accessToken 存储起来
                        GM_setValue('accessToken', accessToken)
                    })
                })
                targetElement.insertBefore(newButton, targetElement.firstChild)
                // Stop observing
                observer.disconnect();
            }
        }
                                             );




        // Start observing
        observer.observe(document, { childList: true, subtree: true });
    })();
};