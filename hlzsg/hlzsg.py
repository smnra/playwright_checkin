
import sys,time,os
from playwright.sync_api import sync_playwright


hezsg_url='https://club.iyogames.cn/?env=web&gameVersion=2144-CN-ZS&lang=zh-CN'

hezsg_login_url='https://club.iyogames.cn/pages/user/login/index?env=web&gameVersion=2144-CN-ZS&lang=zh-CN'



# 同步API （初学者建议先使用同步API）
with sync_playwright() as playwright:

    # 读取cookie

    # 读取UA
    ua = {
        "web": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 "
               "Safari/537.36",
        "app": "com.ss.android.ugc.aweme/110101 (Linux; U; Android 5.1.1; zh_CN; MI 9; Build/NMF26X; "
               "Cronet/TTNetVersion:b4d74d15 2020-04-23 QuicVersion:0144d358 2020-03-24)"
    }

    # 设置浏览器路径

    if sys.platform.startswith('linux'):
        # linux 环境下的chrome浏览器路径
        executable_path = r'/usr/bin/google-chrome-stable'
        # js文件路径
        jsFile = r'/home/runner/work/playwright_checkin/playwright_checkin/stealth.min.js'
    elif sys.platform.startswith('win32'):
        # windows 环境下的chrome浏览器路径
        executable_path = r'E:\\data\\GoogleChromePortable\\App\\Chrome-bin\\chrome.exe'
        # js文件路径
        jsFile = '../stealth.min.js'
    #  插件路径
    path_to_extension = r"E:\\data\\GoogleChromePortable\\Data\\profile\\Default\\Extensions\\keeneegnimhijbnhhcmjpfmmbfceakdi\\1.0.3_0"

    """
    # 设置浏览器属性  launch() 方法启动无痕模式的浏览器  launch_persistent_context() 方法启动有痕模式的浏览器
    browser = playwright.chromium.launch( chromium_sandbox=False,
                                          executable_path=executable_path,  # 指定本机google客户端exe的路径
                                          headless = False,      # 是否隐藏浏览器界面，默认是False
                                          ignore_default_args=["--enable-automation"],
                                          channel="chrome",
                                          )
    # 设置浏览器上下文    # 设置cookie   # 设置UA   # 接受下载
    context = browser.new_context(storage_state=cookieFile,
                                  user_agent=ua["web"],
                                  accept_downloads=True,    # 要想通过这个下载文件这个必然要开  默认是False
                                  )
    """

    browser = playwright.chromium.launch_persistent_context(
            chromium_sandbox=False,
            user_data_dir=r'../userData',  # 指定浏览器用户数据目录，用于保存cookie等信息，默认是None
            executable_path=executable_path,  # 指定本机google客户端exe的路径
            headless=True,  # 是否隐藏浏览器界面，默认是False
            # headless=False,  # 是否隐藏浏览器界面，默认是False
            ignore_default_args=["--enable-automation"],
            viewport={"width": 1920, "height": 1080},  # 指定浏览器窗口大小，默认是1920x1080
            channel="chrome",
            args=[
                "--load-extension={path_to_extension}",  # 加载插件
                # "--disable-extensions-except={path_to_extension}",  # 禁用除指定插件外的所有插件
                "--disable-infobars",  # 禁用信息栏
                "--disable-extensions",  # 禁用插件
                "--disable-notifications",  # 禁用通知
                "--disable-gpu",  # 禁用GPU
                "--no-sandbox",  # 禁用沙盒模式
                "--disable-dev-shm-usage",  # 禁用共享内存
                "--disable-setuid-sandbox",  # 禁用setuid沙盒
                "--disable-webgl",  # 禁用WebGL
                "--disable-popup-blocking",  # 禁用弹窗阻塞
                "--disable-translate",  # 禁用翻译
                "--disable-background-timer-throttling",  # 禁用后台定时器节流
                "--disable-renderer-backgrounding",  # 禁用渲染器后台运行
                "--disable-device-discovery-notifications",  # 禁用设备发现通知
                "--disable-features=site-per-process",  # 禁用站点隔离
                "--disable-features=TranslateUI",  # 禁用翻译界面
                "--disable-features=BlinkGenPropertyTrees",  # 禁用Blink生成属性树
                ]
            )

    # page = browser.new_page()

    page = browser.pages[0]   # 使用第一个标签


    print('当前路径:',os.getcwd())

    # 利用stealth.min.js隐藏selenium特征
    page.add_init_script(path=jsFile)


    #  先访问后台页面 ,然后再打开前台页面  前台页面才能正常登录,否则会提示登录失败
    page.goto(hezsg_login_url, wait_until="domcontentloaded")
    time.sleep(5)
    page.wait_for_selector('xpath=//iframe')
    iframe = page.frame_locator('xpath=//iframe')

    # 登录按钮

    # 输入用户名
    iframe.locator('xpath=//*[@id="root"]/div[1]/div[2]/input').type("wk19628528", timeout=2000)
    # 输入临时密码
    iframe.locator('xpath=//*[@id="root"]/div[1]/div[3]/input').type("my121511", timeout=2000)

    # 点击登录按钮
    iframe.locator('xpath=//*[@id="root"]/div[1]/button').click(timeout=2000)
    try:
        # 选择文本为“每日签到”的标签
        page.wait_for_selector('xpath=//uni-view[text()="每日签到"]')
        checkinLink = page.query_selector('xpath=//uni-view[text()="每日签到"]')
        checkinLink.click(timeout=2000,force=True)        # 点击签到后跳转到 签到页面 有 ifream

        # 等待 iframe 加载完成
        page.wait_for_selector('xpath=//iframe')
        iframe = page.frame_locator('xpath=//iframe')

        # 点击签到按钮
        checkinButton = iframe.locator('xpath=//taro-button-core')
        if checkinButton.text_content()=='已签到':
            print('\n今日已签到,无需再签到!')
        else:
            time.sleep(5)
            checkinButton.click(timeout=2000,force=True) #点击签到
            print('\n签到成功!')

        page.wait_for_selector('xpath=//iframe')
        iframe = page.frame_locator('xpath=//iframe')
        noteTags = iframe.locator('xpath=//*[@class="signin-current-integral hydrated"]').all()
        for tag in noteTags:
            print(tag.text_content())

    except Exception as e:
        print(e)







