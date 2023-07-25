vector <- matrix(c(criteria_table$K1_W2V, criteria_table$K1_RusVec, 
                   criteria_table$K2_W2V, criteria_table$K2_RusVec, 
                   criteria_table$K3_W2V, criteria_table$K3_RusVec, 
                   criteria_table$K4_W2V, criteria_table$K4_RusVec, 
                   criteria_table$K5_W2V, criteria_table$K5_RusVec, 
                   criteria_table$K6_W2V, criteria_table$K6_RusVec,
                   criteria_table$K7_W2V, criteria_table$K7_RusVec,
                   criteria_table$K8_W2V, criteria_table$K8_RusVec,
                   criteria_table$K9_W2V, criteria_table$K9_RusVec,
                   criteria_table$K10_W2V, criteria_table$K10_RusVec,
                   criteria_table$K11_W2V, criteria_table$K11_RusVec,
                   criteria_table$K12_W2V, criteria_table$K12_RusVec,
                   criteria_table$K13_W2V, criteria_table$K13_RusVec), ncol = 26)

criteria_table$Model
vector[,1]
par(mfrow = c(2,4))
for (i in c(1:4)){                    #подставить 5:8, 9:12, 13:16, 17:20, 21:24 для получения визуализаций 
  barplot(vector[,i], names.arg = criteria_table$Model, 
          col = c('#de95a1', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey'))
  }
