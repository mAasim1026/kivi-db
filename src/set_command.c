#include "../include/command_handler.h"
#include "../include/log.h"
#include "../include/sync.h"
#include <sqlite3.h>
#include <stdio.h>
#include <string.h>

extern sqlite3 *db; // Declare external database connection

CommandResponse handle_set(const char *key, const char *value) {
  CommandResponse response = {.success = false, .exit = false};
  const char *insert_query =
      "INSERT INTO key_value_store (key, value) VALUES (?, ?);";
  sqlite3_stmt *stmt;

  if (sqlite3_prepare_v2(db, insert_query, -1, &stmt, NULL) != SQLITE_OK) {
    strcpy(response.error, "Error preparing database statement.\n");
  } else {
    sqlite3_bind_text(stmt, 1, key, -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 2, value, -1, SQLITE_STATIC);

    if (sqlite3_step(stmt) == SQLITE_DONE) {
      strcpy(response.data, "DONE\r\n");
      response.success = true;
      // send data to other nodes
      // SYNC_SET key vale
      SyncResponse response = sync_set(key, value);
      log_message("SYNC_SET complete with success: %d and failures: %d\n",
                  response.sync_success, response.sync_failures);

    } else {
      snprintf(response.error, MAX_RESPONSE_SIZE,
               "Error: Key '%s' already exists.\r\n", key);
    }
    sqlite3_finalize(stmt);
  }

  return response;
}
