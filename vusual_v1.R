criteria_table <- data.table::fread("new_result.csv")


library(ggplot2)
library(hrbrthemes)

# Model <- criteria_table$Model
# Mean_absolute_error <- criteria_table$K1_W2V
# 
# ggplot(criteria_table)+
#   aes (x = Model, y = Mean_absolute_error)+
#   geom_bar(stat='identity')+
#   geom_col(colour ="black")+
#   scale_fill_brewer(palette = "Set1")+
#   labs(title = "Mean_absolute_error. W2V vs RusVectors")
# hrbrthemes::theme_ft_rc()
# 
# 
# Model <- criteria_table$Model
# Mean_absolute_error <- criteria_table$K1_W2V
# par(mfrow = c(2,2))
# ggplot(criteria_table)+
#   aes (x = Model, y = Mean_absolute_error)+
#   geom_bar(stat='identity')+
#   geom_col(colour ="black")+
#   scale_fill_brewer(palette = "Set1")+
#   labs(title = "Mean_absolute_error. W2V vs RusVectors")
# hrbrthemes::theme_ft_rc()


# ggplot(data = criteria_table) +
#   geom_bar(mapping = aes(x=criteria_table$Model, fill = criteria_table$Model), col='black')+
#   theme(legend.position = None)+
#   scale_fill_manual(values=c('blue','red','green','yellow','purple','brown','lightblue'))

par(mfrow = c(2, 2))

barplot(criteria_table$K1_W2V, names.arg = criteria_table$Model,
        col = c('#de95a1', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey')) +
barplot(criteria_table$K1_RusVec, names.arg = criteria_table$Model,
        col = c('#de95a1', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey'))

barplot(criteria_table$K2_W2V, names.arg = criteria_table$Model,
        col = c('#de95a1', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey')) +
  barplot(criteria_table$K2_RusVec, names.arg = criteria_table$Model,
          col = c('#de95a1', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey'))

barplot(criteria_table$K3_W2V, names.arg = criteria_table$Model,
        col = c('#de95a1', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey')) +
  barplot(criteria_table$K3_RusVec, names.arg = criteria_table$Model,
          col = c('#de95a1', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey'))

barplot(criteria_table$K4_W2V, names.arg = criteria_table$Model,
        col = c('#de95a1', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey')) +
barplot(criteria_table$K4_RusVec, names.arg = criteria_table$Model,
          col = c('#de95a1', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey'))

barplot(criteria_table$K5_W2V, names.arg = criteria_table$Model,
        col = c('#c5de95', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey')) +
barplot(criteria_table$K5_RusVec, names.arg = criteria_table$Model,
          col = c('#c5de95', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey'))

barplot(criteria_table$K6_W2V, names.arg = criteria_table$Model,
        col = c("#c5de95", 'grey', 'grey', 'grey', 'grey', 'grey', 'grey')) +
barplot(criteria_table$K6_RusVec, names.arg = criteria_table$Model,
          col = c("#c5de95", 'grey', 'grey', 'grey', 'grey', 'grey', 'grey'))

barplot(criteria_table$K7_W2V, names.arg = criteria_table$Model,
        col = c('#95ded2', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey')) +
  barplot(criteria_table$K7_RusVec, names.arg = criteria_table$Model,
          col = c('#95ded2', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey'))

barplot(criteria_table$K8_W2V, names.arg = criteria_table$Model,
        col = c('#95ded2', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey')) +
  barplot(criteria_table$K8_RusVec, names.arg = criteria_table$Model,
          col = c('#95ded2', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey'))

barplot(criteria_table$K9_W2V, names.arg = criteria_table$Model,
        col = c('#95ded2', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey')) +
  barplot(criteria_table$K9_RusVec, names.arg = criteria_table$Model,
          col = c('#95ded2', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey'))

barplot(criteria_table$K10_W2V, names.arg = criteria_table$Model,
        col = c('#95ded2', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey')) +
  barplot(criteria_table$K10_RusVec, names.arg = criteria_table$Model,
          col = c('#95ded2', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey'))

barplot(criteria_table$K11_W2V, names.arg = criteria_table$Model,
        col = c('#ae95de', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey')) +
barplot(criteria_table$K11_RusVec, names.arg = criteria_table$Model,
          col = c('#ae95de', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey'))


barplot(criteria_table$K12_W2V, names.arg = criteria_table$Model,
        col = c('#ae95de', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey')) +
  barplot(criteria_table$K12_RusVec, names.arg = criteria_table$Model,
          col = c('#ae95de', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey'))

barplot(criteria_table$K13_W2V, names.arg = criteria_table$Model,
        col = c('#de95a1', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey')) +
  barplot(criteria_table$K13_RusVec, names.arg = criteria_table$Model,
          col = c('#de95a1', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey'))




