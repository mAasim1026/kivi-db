#include "../include/command_handler.h"
#include <sqlite3.h>
#include <stdio.h>
#include <string.h>

extern sqlite3 *db; // Declare external database connection

CommandResponse handle_sync_update(const char *key, const char *value) {
    CommandResponse response = {.success = false, .exit = false};
    const char *update_query = "UPDATE key_value_store SET value = ? WHERE key = ?;";
    sqlite3_stmt *stmt;

    if (sqlite3_prepare_v2(db, update_query, -1, &stmt, NULL) != SQLITE_OK) {
        strcpy(response.error, "Error preparing database statement.\n");
    } else {
        sqlite3_bind_text(stmt, 1, value, -1, SQLITE_STATIC);
        sqlite3_bind_text(stmt, 2, key, -1, SQLITE_STATIC);handle_set(key, value);

        if (sqlite3_step(stmt) == SQLITE_DONE) {
            if (sqlite3_changes(db) > 0) {
                strcpy(response.data, "Updated successfully.\r\n");
                response.success = true;
            } else {
                strcpy(response.error, "Error: Key not found.\r\n");
            }
        } else {
            strcpy(response.error, "Failed to update key.\n");
        }
        sqlite3_finalize(stmt);
    }

    return response;
}
