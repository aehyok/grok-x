#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <curl/curl.h>

#define LOG_FILE "/var/log/cpolar/access.log"
#define NTFY_URL "https://ntfy.sh/your_cpolar_channel"  // 替换为实际的 ntfy 频道地址

// 发送 ntfy.sh 推送通知
void send_notification(const char *msg) {
    CURL *curl = curl_easy_init();
    if (curl) {
        curl_easy_setopt(curl, CURLOPT_URL, NTFY_URL);
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, msg);
        curl_easy_setopt(curl, CURLOPT_TIMEOUT, 10L);
        curl_easy_perform(curl);
        curl_easy_cleanup(curl);
    }
}

// 获取本机的 SSH ed25519 公钥指纹
void get_ssh_fingerprint(char *output, size_t max_len) {
    FILE *fp = popen("ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub 2>/dev/null", "r");
    if (fp) {
        if (fgets(output, max_len, fp) != NULL) {
            output[strcspn(output, "\r\n")] = 0; // 去除换行符
        }
        pclose(fp);
    }
}

// 核心日志监控与分析逻辑
void watch_cpolar_log() {
    char command[256];
    snprintf(command, sizeof(command), "tail -n0 -F '%s' 2>/dev/null", LOG_FILE);

    FILE *fp = popen(command, "r");
    if (!fp) {
        perror("popen failed");
        return;
    }

    char line[1024];
    while (fgets(line, sizeof(line), fp) != NULL) {
        // 捕捉 cpolar 端点启动或隧道更新日志 (含有 StartProxy 或 5.tcp.cpolar.cn)
        if (strstr(line, "StartProxy") || strstr(line, "5.tcp.cpolar.cn") || strstr(line, "tcp://")) {
            char host_fp[256] = {0};
            get_ssh_fingerprint(host_fp, sizeof(host_fp));

            char notify_msg[2048];
            snprintf(notify_msg, sizeof(notify_msg),
                     "🚀 [cpolar Endpoint Reporter]\nLog: %sHost Key: %s",
                     line, host_fp);

            send_notification(notify_msg);
        }
    }
    pclose(fp);
}

int main(int argc, char *argv[]) {
    curl_global_init(CURL_GLOBAL_DEFAULT);

    if (argc > 1 && strcmp(argv[1], "--watch") == 0) {
        watch_cpolar_log();
    } else {
        printf("Usage: %s --watch\n", argv[0]);
    }

    curl_global_cleanup();
    return 0;
}
