criteria_table <- data.table::fread("new_result.csv")

library(ggplot2)
library(hrbrthemes)
library(ggpubr)

Model <- criteria_table$Model
Mean_absolute_error_W2V <- criteria_table$K13_W2V
Mean_absolute_error_RusV <- criteria_table$K13_RusVec

visualization_1 <- ggplot(criteria_table, aes(x = Model, y = Mean_absolute_error_W2V))+
  geom_bar(stat='identity', aes(fill = Model))+
  labs(title = "Mean absolute error", subtitle = "Word2Vec")+
  scale_fill_manual(values = c("#bdf0bd", "#91ba91", "#84b884", "#689968", '#537053', "#315731", "red"))+
  theme_ft_rc(axis_title_just = "center", axis_text_size = 8, axis_title_size = 15)
  

visualisation_2 <- ggplot(criteria_table, aes(x = Model, y = Mean_absolute_error_RusV))+
  geom_bar(stat='identity', aes(fill = Model))+
  labs(title = "Mean absolute error", subtitle = "RusVectors")+
  scale_fill_manual(values = c("#bdf0bd", "#91ba91", "#84b884", "#689968", '#537053', "#315731", "red"))+
  theme_ft_rc(axis_title_just = "center", axis_text_size = 8, axis_title_size = 15)

vis <- ggarrange(visualization_1, visualisation_2)

annotate_figure(vis, "Среднее абсолютное отклонение для итогового балла сочинений")

