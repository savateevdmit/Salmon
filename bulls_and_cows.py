import pymorphy2

flag = True


def bulls_and_cows(entry, number):
    def count_of_bull_and_cows(number, entry):
        cow, bull = 0, 0
        for i in range(len(number)):
            if number[i] == entry_history[i]:
                bull += 1
            elif number[i] in entry_history:
                cow += 1
        return cow, bull

    morph = pymorphy2.MorphAnalyzer()

    def morph_cows_and_bulls(morph_cows='корова', morph_bulls='бык'):
        m_cows = morph.parse(morph_cows)[0]
        cows_ = m_cows.make_agree_with_number(counts[0]).word
        m_bulls = morph.parse(morph_bulls)[0]
        buls_ = m_bulls.make_agree_with_number(counts[1]).word
        return cows_, buls_

    entry_history = []
    while entry_history != number:
        entry_history = []
        for i in str(entry):
            entry_history.append(int(i))
        #  entry_history.extend(str(entry))
        counts = count_of_bull_and_cows(number, entry)
        morph_ = morph_cows_and_bulls()
        if entry_history != number:
            return 'вы не угадали(, но у вас {0} {1} и {2} {3}! '.format(counts[1], morph_[1], counts[0], morph_[0])
            break

        if entry_history == number:
            return 'вы дали правильный ответ!'
            break

# bulls_and_cows(int(input()))
