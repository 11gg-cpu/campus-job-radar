# Campus Job Radar

一个独立的校园招聘 AI skill：根据简历与求职偏好收集岗位，完成 S/A/B 匹配、永久去重和投递进度维护。

## Skill

`skill/campus-job-radar/`

支持 skill 文件的 AI agent 可以复制该目录并按产品说明启用。不支持安装 skill 的 AI，也可以读取 `SKILL.md`、模板和脚本后执行相同工作流。

## 验证

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py skill/campus-job-radar
python3 -m compileall -q skill/campus-job-radar
python3 skill/campus-job-radar/scripts/job_ledger.py normalize "公司名" "岗位名"
```

## 安全边界

- 不自动投递或登录招聘网站。
- 不保存密码、Cookie、token、身份证号或完整住址。
- 岗位信息会变化，投递前应回到官方招聘页核验。

## License

MIT
