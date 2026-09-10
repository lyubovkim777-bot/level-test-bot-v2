/**
 * Вставьте этот код в Google Таблицу через:
 * Extensions (Расширения) -> Apps Script -> вставить сюда, заменив
 * содержимое файла -> Deploy (Развернуть) -> New deployment ->
 * Type: Web app -> Execute as: Me -> Who has access: Anyone ->
 * Deploy -> скопировать URL веб-приложения.
 *
 * Этот URL нужно вставить в переменную окружения GOOGLE_SCRIPT_URL бота.
 *
 * Никакого Cloud Console, API ключей и сервисных аккаунтов не требуется.
 */

var SHEET_NAME = "Заявки";
var HEADER_ROW = ["Дата", "Имя", "Телефон", "Telegram username", "Баллы", "«Не знаю» (кол-во)", "Уровень"];

function doPost(e) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAME);
  }
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(HEADER_ROW);
  }

  var data = JSON.parse(e.postData.contents);
  sheet.appendRow([
    data.date || new Date(),
    data.name || "",
    data.phone || "",
    data.username || "",
    data.score || "",
    data.idk_count || 0,
    data.level || ""
  ]);

  return ContentService
    .createTextOutput(JSON.stringify({ status: "ok" }))
    .setMimeType(ContentService.MimeType.JSON);
}

function doGet(e) {
  return ContentService.createTextOutput("Bot webhook is alive");
}
