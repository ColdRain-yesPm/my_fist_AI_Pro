flowchart TD
    subgraph S1["① 入口与合规闸门（F0 / F1 / F2）"]
        START([开始])
        ENTRY{"入口类型"}
        A1["点击「开始录音」"]
        A2{"涉及外部参会方?"}
        A3["记录告知时间与方式<br/>提供告知话术一键复制"]
        A4{"已获参会人同意?"}
        A5["阻断：不开始录音<br/>提示先获取同意"]
        STOP([流程终止])
        A6{"参会人名单已填?"}
        A7["提示必填<br/>坚持继续则降级为「不做负责人推断」"]
        A8["开始录音"]
        B1["上传音频文件"]
        B2{"提供参会人名单?"}
        B3["上传并启动任务"]
        B4["上传并启动任务<br/>标记：不做负责人推断"]
        A9["录音中：显示「录音中」标识<br/>禁止静默 / 后台录音"]
        A10{"录音是否中断?"}
        A11["F2 恢复已录音频<br/>提示已恢复时长"]
        A12["停止录音"]
        A13["本地保存 + 自动上传任务队列"]
        RET["音频 30 天后自动删除<br/>纪要文本与行动项长期保留"]
    end

    subgraph S2["② 转写与标定（F4 / F5 / F6）"]
        T1["ASR 转写：时间戳 + 说话人分离"]
        T2{"存在未标定说话人?"}
        T3["提示从参会人名单点选<br/>一次绑定全程复用"]
        T4["用户校对转写文本<br/>校正人名 / 术语 / 口音"]
    end

    subgraph S3["③ 生成与抽取（F7 – F10）"]
        G1["生成纪要：摘要 / 议题 / 决议"]
        G2["抽取行动项"]
        G2B{"是否抽到行动项?"}
        G2C["action_items = 空数组<br/>提示「本次未识别到行动项」"]
        G3{"负责人是否可确定?"}
        G4["owner = 明确值<br/>owner_source = roster_match"]
        G5["owner = 推断值<br/>owner_source = context_infer<br/>不自动指派"]
        G6["owner = null<br/>owner_source = unrecognized<br/>标记「待确认」"]
        G8{"截止时间是否明确?"}
        G9["due_date = 归一化日期<br/>due_source 标注"]
        G10["due_date = null<br/>进入 open_questions"]
        G11["置信度可视化：高 / 中 / 低着色<br/>可跳转原文时间戳核对"]
    end

    subgraph S4["④ 确认与交付（F0 / F11 / F12）"]
        H1{"用户是否确认终稿?"}
        H2["编辑 / 改指派 / 改期<br/>记录编辑量 F11"]
        H3["生成终稿"]
        H4["权限：默认仅上传者可见<br/>可显式分享给参会人"]
        E1{"导出目标"}
        E2{"钉钉 API 写权限可用?"}
        E3{"人名 → userid 遇同名?"}
        E4["弹窗要求用户确认<br/>禁止静默选择"]
        E5["写入钉钉多维表格"]
        E6["降级：导出可直导 CSV"]
        E7["通用导出<br/>Markdown / 剪贴板"]
        END2([结束])
    end

    START --> ENTRY
    ENTRY -->|"场景 A：会中现场录音"| A1
    ENTRY -->|"场景 B：会后已有文件"| B1

    A1 --> A2
    A2 -->|"是（场景 C）"| A3
    A2 -->|"否"| A4
    A3 --> A4
    A4 -->|"否"| A5
    A5 --> STOP
    A4 -->|"是"| A6
    A6 -->|"否"| A7
    A6 -->|"是"| A8
    A7 --> A8

    B1 --> B2
    B2 -->|"是"| B3
    B2 -->|"否"| B4

    A8 --> A9
    A9 --> A10
    A10 -->|"崩溃 / 断电"| A11
    A10 -->|"正常"| A12
    A11 --> A12
    A12 --> A13
    A13 -.->|"异步 30 天计时"| RET

    A13 --> T1
    B3 --> T1
    B4 --> T1

    T1 --> T2
    T2 -->|"是"| T3
    T2 -->|"否"| T4
    T3 --> T4

    T4 --> G1
    G1 --> G2
    G2 --> G2B
    G2B -->|"0 条"| G2C
    G2B -->|"1 条及以上"| G3
    G3 -->|"原文明确指派"| G4
    G3 -->|"上下文推断"| G5
    G3 -->|"听不清 / 无人认领"| G6
    G4 --> G8
    G5 --> G8
    G6 --> G8
    G8 -->|"显式时间或可归一化相对时间"| G9
    G8 -->|"模糊表达（尽快 / 下周再说）"| G10
    G9 --> G11
    G10 --> G11

    G2C --> H1
    G11 --> H1
    H1 -->|"需修改"| H2
    H2 --> H1
    H1 -->|"确认"| H3

    H3 --> H4
    H4 --> E1
    E1 -->|"钉钉多维表格"| E2
    E2 -->|"可用"| E3
    E2 -->|"不可用"| E6
    E3 -->|"是"| E4
    E3 -->|"否"| E5
    E4 --> E5
    E5 --> END2
    E1 -->|"Markdown / 剪贴板"| E7
    E7 --> END2
    E6 --> END2

    style A5 fill:#ffe0e0,stroke:#c0392b,stroke-width:2px
    style STOP fill:#ffe0e0,stroke:#c0392b,stroke-width:2px
    style A7 fill:#fff4d6,stroke:#c99a00
    style G6 fill:#fff4d6,stroke:#c99a00
    style G10 fill:#fff4d6,stroke:#c99a00
    style G2C fill:#fff4d6,stroke:#c99a00
    style G4 fill:#e8f6e8,stroke:#2e8b57
    style G5 fill:#e8f6e8,stroke:#2e8b57
    style T4 fill:#e8eefc,stroke:#2f5fa8
    style H1 fill:#e8eefc,stroke:#2f5fa8
