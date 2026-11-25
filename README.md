# Deadline SO 停止封存结果

本仓库保存 `Deadline_SO_Balanced_Final.zip` 的完整原始字节。归档分为 6 个 Git LFS 分卷；按顺序合并即可得到原 ZIP，未重新压缩或改变内容。

- 原 ZIP：9,593,761,023 字节。
- SHA-256：`ebad2ab1b473d0e8d268ecf45197e8eed179bb5d3c71d91caca0d7ab4519cb68`。
- 分卷顺序、大小与哈希见 `archive_manifest.json`。
- 实验已停止；本仓库不会自动运行实验。

## 下载与还原

安装 Git LFS 后执行：

```sh
git clone git@github.com:kynecubus/res.git
cd res
git lfs pull
python3 restore_archive.py
```

Windows 可将 `python3` 换为 `python`。还原需要约 9.59 GB 额外磁盘空间。脚本逐卷核对 SHA-256，再核对合并后的原 ZIP 哈希，拒绝覆盖已有目标文件。

仅校验、不生成 ZIP：

```sh
python3 restore_archive.py --verify-only
```

## 封存范围

ZIP 包含中文 22 项停止封存报告、实际处理后的输入、必要源码与 Patch、配置、结构化 metrics、正确性和输入一致性证据、图表及复现材料，不包含原始 SO 源文件。

50K / E0、500K / E1–E7 的已执行结果已封存。Full / E8 有 49 次完成、11 次超时、1 次用户中止，其余取消；E9 Arrival 未执行。最终最优配置尚未确定。18 份此前被原验证流程删除的临时 50K 测试样本仅保留原验证结果及哈希，ZIP 报告明确说明。已记录性能 worker 的实际输入全部封存。
