import random

# 建立撲克牌花色與點數
# 黑桃spades、紅心hearts、方塊diamonds、梅花clubs
suits = ["spade", "heart", "diamond", "club"]
ranks = {
    "A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
    "7": 7, "8": 8, "9": 9, "10": 10, "J": 11, "Q": 12, "K": 13
}

def create_deck():
    """
    建立 52 張撲克牌牌組 (含花色與數字)
    例如: ("spade", "A"), ("heart", "7")...
    """
    deck = []
    for s in suits:
        for r in ranks:
            deck.append((s, r))
    random.shuffle(deck)
    return deck

def card_effect(card, current_sum):
    """
    根據牌的種類與花色，執行對應功能牌效果，
    回傳 (new_sum)。

    規則：(原先99規則4為迴轉、5為指定玩家出牌，為方便，以加數值簡化)
    1) 黑桃A -> 歸零 (new_sum = 0)
    2) A（非黑桃）-> +1
    3) 2,3,4,5,6,7,8,9 -> 對應加 val
    4) 10 -> 決定 +10 或 -10
    5) J -> 跳過
    6) Q -> 決定 +20 或 -20
    7) K -> 無論目前累計，數值直接 = 99
    """
    suit, rank = card
    val = ranks[rank]

    # 預設維持 current_sum
    new_sum = current_sum

    # 黑桃A -> 歸零
    if rank == "A" and suit == "spade":
        new_sum = 0
    # A（非黑桃）-> +1
    elif rank == "A":
        new_sum = current_sum + 1
    # 2,3,4,5,6,7,8,9 -> 對應加 val
    elif rank in ["2", "3", "4", "5", "6", "7", "8", "9"]:
        new_sum = current_sum + val
    # 10 -> +10 或 -10 (另外處理，先pass)
    elif rank == "10":
        pass
    # J -> 跳過 (目前累計數值不變)
    elif rank == "J":
        new_sum = current_sum
    # Q -> +20 或 -20 (另外處理，先pass)
    elif rank == "Q":
        pass
    # K -> = 99
    elif rank == "K":
        new_sum = 99

    return new_sum

def play_99():
    # 建立卡牌並分給玩家與電腦 (各抽 5 張)
    deck = create_deck()
    player_hand = deck[:5]
    computer_hand = deck[5:10]
    deck_index = 10
    
    current_sum = 0
    is_player_turn = True  # 先由玩家開始
    game_over = False

    while not game_over:
        print("\n" + ">" * 50)
        print(f"目前累計：{current_sum}")
        print("<" * 50)
        print("=" * 50)        
        print(f"玩家手牌：{player_hand}")
        print(f"電腦手牌（只顯示張數）：{len(computer_hand)} 張")
        print("=" * 50)

        # 檢查誰的回合
        if is_player_turn:
            # === 玩家出牌 ===
            print("***** 輪到玩家出牌 *****")
            for i, card in enumerate(player_hand):
                print(f"{i}. ({card[0]}-{card[1]})", end="  ")
            print("")

            try:
                choice = input("請選擇要出的牌（輸入選項0/1/2/3/4，若想退出請輸入q）：")
                
                # 當玩家想退出遊戲時
                if choice == "q":
                    ask = input("不想繼續玩了嗎？（輸入「y」退出遊戲；不是則輸入「n」）：")
                    if ask == "y":
                        game_over = True
                    elif ask == "n":
                        continue
                    else:
                        print("輸入錯誤，請重新輸入")
                        continue
                
                # 玩家輸入錯誤處理
                choice = int(choice)
                if choice < 0 or choice >= len(player_hand):
                    raise IndexError
                
                card = player_hand.pop(choice)
            # 分開處理錯誤情況
            except ValueError:
                # print("請輸入0/1/2/3/4/q等有效選項")
                continue
            except IndexError:
                print("請輸入0/1/2/3/4/q等有效選項")
                continue

            s, r = card
            
            # 若是 10 -> 玩家選 +10 或 -10
            if r == "10":
                while True:
                    player = input("玩家出「10」，請輸入「+10」或「-10」：")
                    if player == "+10" or player == "-10":
                        # 設計防呆，避免累計小於0
                        test_sum = current_sum + int(player)
                        if test_sum < 0:
                            print("輸入錯誤，目前累計小於0，請重新出牌")
                            continue
                        else:
                            new_sum = test_sum
                            break
                    else:
                        print("不要不知好歹，輸入錯誤，請重新出牌")

            # 若是 Q -> 玩家選 +20 或 -20
            elif r == "Q":
                while True:
                    player = input("玩家出「20」，請輸入「+20」或「-20」：")
                    if player == "+20" or player == "-20":
                        # 設計防呆，避免累計小於0
                        test_sum = current_sum + int(player)
                        if test_sum < 0:
                            print("輸入錯誤，目前累計小於0，請重新出牌")
                            continue
                        else:
                            new_sum = test_sum
                            break
                    else:
                        print("不要不知好歹，輸入錯誤，請重新出牌")

            # 若是 J -> 出牌者本回合跳過，累計數值不變
            elif r == "J":
                new_sum = current_sum
                print("***** 玩家跳過本回合 *****") 
            else:
                new_sum = card_effect(card, current_sum)

            print(f"玩家出牌：({s}-{r})")

            # 檢查是否爆炸
            if new_sum > 99:
                print("超過 99 了！玩家輸了！電腦獲勝！")
                game_over = True
            else:
                # 更新累計
                current_sum = new_sum

                # 無條件抽一張牌（若牌庫還有）
                if deck_index < len(deck):
                    player_hand.append(deck[deck_index])
                    deck_index += 1

                # 結束玩家回合，切換給電腦
                is_player_turn = False

        else:
            # === 電腦回合 ===
            print("***** 輪到電腦出牌 *****")
            chosen_card_index = None

            # 電腦嘗試找「不會爆」的牌
            for i, c in enumerate(computer_hand):
                s2, r2 = c
                test_sum = current_sum

                # 若是 10，電腦簡單邏輯：先嘗試 +10，若爆就 -10
                if r2 == "10":
                    if test_sum + 10 <= 99:
                        test_sum += 10
                    else:
                        test_sum -= 10
                # 若是 Q，電腦簡單邏輯：先嘗試 +20，若爆就 -20
                elif r2 == "Q":
                    if test_sum + 20 <= 99:
                        test_sum += 20
                    else:
                        test_sum -= 20
                # 若是 J -> 電腦跳過本回合（test_sum 不變）
                elif r2 == "J":
                    pass
                else:
                    test_sum = card_effect(c, test_sum)

                # 如果不爆就出這張
                if test_sum <= 99:
                    chosen_card_index = i
                    break

            if chosen_card_index is None:
                # 如果都會爆，隨便出一張
                chosen_card_index = random.randint(0, len(computer_hand) - 1)

            card_c = computer_hand.pop(chosen_card_index)
            s3, r3 = card_c

            # 電腦正式計算 new_sum
            if r3 == "10":
                if current_sum + 10 <= 99:
                    new_sum = current_sum + 10
                else:
                    new_sum = current_sum - 10
            elif r3 == "Q":
                if current_sum + 20 <= 99:
                    new_sum = current_sum + 20
                else:
                    new_sum = current_sum - 20
            elif r3 == "J":
                new_sum = current_sum
                print("***** 電腦跳過本回合 *****")                 
            else:
                new_sum = card_effect(card_c, current_sum)

            print(f"電腦出牌：({s3}-{r3})")

            # 檢查爆炸
            if new_sum > 99:
                print("超過 99 了！電腦輸了！玩家獲勝！")
                game_over = True
            else:
                current_sum = new_sum

                # 無條件抽一張牌（若牌庫還有）
                if deck_index < len(deck):
                    computer_hand.append(deck[deck_index])
                    deck_index += 1

                # 電腦回合結束，下一輪換玩家
                is_player_turn = True

    print("\n遊戲結束！")

# 主程式示範
if __name__ == "__main__":
    option = input("按 Enter 開始遊戲，或輸入「q/Q」離開：")
    if option == "q" or option == "Q":
        print("\n遊戲結束！")
        exit()
    else:
        play_99()
