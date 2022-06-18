// flash妫€娴�
function flashCheck() {
    var flag = false;
    if (window.ActiveXObject) {
        try {
            var swf = new ActiveXObject("ShockwaveFlash.ShockwaveFlash");
            if (swf) {
                flag = true;
            }
        } catch (e) {}
    } else {
        try {
            var swf = navigator.plugins["Shockwave Flash"];
            if (swf) {
                flag = true;
            }
        } catch (e) {}
    }
    return flag;
}
// 璁剧疆swf涓烘湰鍦扮殑
function setLocalFlashSwf() {
    let swfName = "video-js.swf";
    let indexJs = "videojs-flvjs-expand.js";
    let indexJsSrc = $(`script[src*='/${indexJs}']`)[0].src;
    let _swf = indexJsSrc.replace(indexJs, swfName);
    videojs.options.flash.swf = _swf;
}
// 杩愯妫€娴�
function expandExecuteCheck(id) {
    //鍒ゆ柇鏈夋晥娴佹湁鍑犵
    $(`#${id}>source[src='']`).remove();
    let useVideo = $(`#${id}>source[src]`);
    if (useVideo.length === 0) {
        //濡傛灉娌℃湁鍙挱鏀剧殑鍦板潃 鍒欓€€鍑�
        alert("璇疯嚦灏戜紶鍏ヤ竴涓挱鏀惧湴鍧€");
        return false;
    } else {
        // 娴忚鍣ㄨ嚜甯︾殑
        const DEFAULT_TYPE = ["video/mp4", "video/webm", "video/ogg"];
        const DEFAULT_RULES = [".mp4", ".webm", ".ogg"];
        // 鍙挱鏀剧殑鏍煎紡
        const VIDEO_TYPE = [
            "application/x-mpegURL",
            "rtmp/flv",
            "video/x-flv",
            ...DEFAULT_TYPE,
        ];
        const VIDEO_RULES = [".m3u8", "rtmp:", ".flv", ...DEFAULT_RULES];
        const TECH_TYPE = ["html5", "flash", "flvjs"];

        // let techOrder = ["html5"];
        let techOrder = []; //
        let sourceMatch = {};
        let matchObj = {};

        // 璧嬪€�
        VIDEO_TYPE.forEach(function (val, index) {
            sourceMatch[VIDEO_TYPE[index]] = VIDEO_RULES[index];
        });

        // 妫€娴嬮〉闈腑鐨剆ource鍜宼ype
        for (let i = 0; i < useVideo.length; i++) {
            // current source type
            let cSource_type = useVideo[i]["type"];
            let cSource_typeLower = cSource_type.toLowerCase();
            // src
            let cSource_src = useVideo[i]["src"];
            let cSource_srcLower = cSource_src.toLowerCase();

            //鏄惁鏈夎繖涓猻ource type
            if (cSource_type && sourceMatch.hasOwnProperty(cSource_typeLower)) {
                let isMatch = cSource_srcLower.includes(sourceMatch[cSource_typeLower]);
                //has
                if (isMatch) {
                    //绗﹀悎鏉′欢
                    console.info(`info:`, `[${cSource_src}]`, `[${cSource_type}]`);
                    matchObj[`${cSource_type}`] = `${cSource_src}`;
                    // 鍒ゆ柇order
                    switch (cSource_type) {
                        case VIDEO_TYPE[0]:
                        case VIDEO_TYPE[1]:
                            techOrder.push(TECH_TYPE[1]);
                            break;
                        case VIDEO_TYPE[2]:
                            techOrder.push(TECH_TYPE[2]);
                            break;
                    }
                } else {
                    //涓嶇鍚堢殑 remove
                    let currentStr = `#${id}>source[src='${cSource_src}'][type='${cSource_type}']`;
                    $(currentStr).remove();
                    console.error(
                        `ERROR:`,
                        `[${cSource_src}]`,
                        `[${cSource_type}]`,
                        `[娴佸湴鍧€涓嶇鍚堟牸寮忥紝鏃犳硶鎾斁]`
                    );
                }
            }
        }
        // 鍒ゆ柇鏄惁閮戒笉绗﹀悎
        let useVideo2 = $(`#${id}>source[src]`);
        if (useVideo2.length === 0) {
            // 濡傛灉娌℃湁鍙挱鏀剧殑鍦板潃 鍒欓€€鍑�
            alert("娌℃湁绗﹀悎鏉′欢鐨勬挱鏀惧湴鍧€锛屾挱鏀惧け璐�");
            return false;
        } else {
            techOrder = Array.from(new Set(techOrder));
            // 鍒ゆ柇flash鏄惁瀛樺湪
            let f_ok = flashCheck();
            if (!f_ok && techOrder.includes(TECH_TYPE[1])) {
                delete techOrder[techOrder.indexOf(TECH_TYPE[1])];
                delete matchObj[VIDEO_TYPE[0]];
                delete matchObj[VIDEO_TYPE[1]];
                // 鍒犻櫎鍚庢病鏈夋挱鏀惧湴鍧€灏辨彁绀�
                if (Object.keys(matchObj).length === 0) {
                    alert("娴忚鍣ㄦ病鏈塮lash 鏃犳硶鎾斁");
                    return false;
                }
            }
            /**
             *浼樺厛绾�
             *  涔嬪墠鏄� html5 > flash > flv
             *  鐜板湪 flash > flv > html5
             */
            techOrder.push(TECH_TYPE[0]); //
            console.info(`techOrder:[${techOrder}]`);
            // 杩斿洖techOrder 鏁扮粍鍙兘鏈夌┖鍏冪礌浣嗘槸涓嶅奖鍝�
            return techOrder;
        }
    }
}
// 鍒濆鍖�
function expandVideoInit(id) {
    //swf鍒囨崲涓烘湰鍦扮殑
    setLocalFlashSwf()
    // 杩愯妫€娴�
    let result = expandExecuteCheck(id);
    if (!result) {
        return;
    }
    console.time("VIDEOJS");
    videojs(
        id,
        {
            techOrder: result,
            autoplay: true,
            muted: true,
        },
        function onPlayerReady() {
            videojs.log("Your player is ready!");
            console.timeEnd("VIDEOJS");
            // flvjs瀵硅薄
            console.log(this.tech({ IWillNotUseThisInPlugins: true }));
            let { flvPlayer } = this.tech({
                IWillNotUseThisInPlugins: true,
            });
            if (flvPlayer) {
                flvPlayer.play();
            }
        }
    );
}
// 鍒囨崲鍦板潃
function expandVideoSrc(obj) {
    let videoElement = document.getElementById("videojs-flvjs-player_Flvjs_api");
    if (!videoElement) {
        // 涓嶅瓨鍦ㄥ氨鏄痜lash
        // videojs鐨勪慨鏀�
        videojs(obj.id, {}).ready(function () {
            var myPlayer = this;
            myPlayer.src(obj.url);
            myPlayer.play();
        });
    } else {
        // 鑾峰彇鐖跺厓绱犵劧鍚庡垹闄や箣鍓嶇殑dom锛屽啀閲嶆柊鍒涘缓涓€涓�;
        let parentDiv = document.getElementById(obj.id).parentElement;
        videojs(obj.id).dispose();
        let str = `<video id="${obj.id}" class="video-js" controls muted>
                      <source
                        src="${obj.url}"
                        type="video/x-flv"
                      /></video>`;
        $(parentDiv).append(str);
        // 鎵ц
        expandVideoInit(obj.id);
    }
}