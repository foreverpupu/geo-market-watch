# scripts 目录边界说明
## 定位
本目录为开发工具脚本（dev utility），包含lint、测试、打包、迁移等通用开发工具
## 与包内脚本边界
geo_market_watch/scripts/为业务执行脚本，面向正式功能运行；本目录脚本仅面向开发流程使用
## 正式入口
用户正式使用统一通过pyproject.toml暴露的gmw-* CLI，不直接调用本目录脚本
