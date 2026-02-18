# 台電兩段式時間電價 (Taiwan Power Price)

[![HACS Default](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/release/yourname/taiwan-power-price.svg)](https://github.com/yourname/taiwan-power-price/releases)
[![GitHub License](https://img.shields.io/github/license/yourname/taiwan-power-price.svg)](LICENSE)

台灣電力公司兩段式時間電價感測器，適用於 Home Assistant。

## 功能

- ✅ 自動夏月/非夏月電價切換 (6/1-9/30)
- ✅ 尖峰/離峰時段自動判斷
- ✅ 國定假日自動辨識
- ✅ 農曆春節、端午、中秋自動計算
- ✅ 無需 API Key，完全離線運作

## 安裝

### 透過 HACS (建議)

1. 打開 HACS
2. 搜尋「台電兩段式時間電價」
3. 安裝

### 手動安裝

1. 複製 `custom_components/taiwan_power_price` 到 `config/custom_components/`
2. 重啟 Home Assistant

## 電價資訊

### 夏月 (6/1-9/30)

| 類型 | 時間 | 單價 |
|------|------|------|
| 平日尖峰 | 09:00-24:00 | $5.16/度 |
| 平日離峰 | 00:00-09:00 | $2.06/度 |
| 週末/離峰日 | 全日 | $2.06/度 |

### 非夏月

| 類型 | 時間 | 單價 |
|------|------|------|
| 平日尖峰 | 06:00-11:00, 14:00-24:00 | $4.93/度 |
| 平日離峰 | 00:00-06:00, 11:00-14:00 | $1.99/度 |
| 週末/離峰日 | 全日 | $1.99/度 |

### 離峰日清單

- 元旦 (1/1)
- 春節（除夕至初五）
- 和平紀念日 (2/28)
- 兒童節 (4/4)
- 清明節 (4/4-4/5)
- 勞動節 (5/1)
- 端午節（農曆五月五日）
- 中秋節（農曆八月十五日）
- 國慶日 (10/10)

## 實體

整合會建立一個感測器 `sensor.taiwan_power_price`，屬性如下：

| 屬性 | 說明 |
|------|------|
| `native_value` | 當前電價（元/度） |
| `is_summer` | 是否為夏月 |
| `is_holiday` | 是否為離峰日 |
| `is_weekend` | 是否為週末 |
| `price_type` | `peak` 或 `off_peak` |
| `period` | `summer` 或 `non_summer` |

## Lovelace 範例

### 儀表板卡片

```yaml
type: entities
title: 當前電價
entities:
  - entity: sensor.taiwan_power_price
    name: 電價
    secondary_info: attribute.price_type
```

### 儀表板 gauge

```yaml
type: gauge
entity: sensor.taiwan_power_price
min: 0
max: 6
unit: 元/度
```

## 支援

- [問題回報](https://github.com/yourname/taiwan-power-price/issues)
- [功能請求](https://github.com/yourname/taiwan-power-price/discussions)

## 授權

MIT License
