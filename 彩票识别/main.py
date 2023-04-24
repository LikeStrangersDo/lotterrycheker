from lotterychecker import recognize_text, get_lottery_numbers, check_lottery_numbers


# 主函数，调用以上两个函数，实现对彩票的验证
if __name__ == '__main__':
    # 图像文件路径
    image_path = '多注实例1.jpg'
    # 识别图像中的文字信息
    lottery = recognize_text(image_path)
    # 通过期号查询中奖号码
    winning_numbers = get_lottery_numbers(issue=lottery[0])
    # 将开奖结果以字典形式存储
    winning_numbers = {'red_balls': winning_numbers[0],
                       'blue_ball': winning_numbers[1]}
    # 循环查询中奖情况
    for y in range(len(lottery[1])):
        print('第{}注彩票红球为：{}\n'
              '蓝球为：{}\n'
              '倍数为：{}'.format(y + 1, lottery[1][y]['red_balls'], lottery[1][y]['blue_ball'], lottery[1][y]['multiple']))

        # 打印中奖核对结果
        print('第{}注中奖情况如下：\n'.format(y+1), check_lottery_numbers(lottery[1][y], winning_numbers))