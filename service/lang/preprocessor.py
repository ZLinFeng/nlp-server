# coding=utf-8
"""
@file    preprocessor
@date    2022/6/28 10:32 AM
@author  zlf
"""
import abc

import utils

from service.lang import lang_char


class IPreprocessor(metaclass=abc.ABCMeta):

    @staticmethod
    def is_cjk(char: str) -> bool:
        """
        :param char: 输入的字符或者字符串
        :return: 是否属于中日韩数据集
        """
        if len(char) != 1:
            return False
        return "\u3400" <= char <= "\u4DBF" or "\u4E00" <= char <= "\u9FFF" or "\uF900" <= char <= "\uFAFF"

    @staticmethod
    def word_spliter(text: str) -> list[str]:
        """
        :param text: 输入的文本
        :return: 分词后的列表
        """
        words = []
        for word in text.split(" "):
            item = ""
            if word.startswith("@") or word.startswith("#"):
                words.append(word)
                continue
            for char in word:
                if IPreprocessor.is_cjk(char):
                    if len(item) > 0:
                        words.append(item)
                    words.append(char)
                    item = ""
                else:
                    item += char
            if len(item) > 0:
                words.append(item)
        return words

    @staticmethod
    def word_filter(text: str) -> str:
        """
        :param text: 输入的文本
        :return: 过滤文本里面无效的单词并返回文本
        """
        if utils.is_empty(text):
            return text
        text = text.lower().replace("\n", " ").replace("\t", " ")
        words = []
        for word in IPreprocessor.word_spliter(text):
            word = word.strip(",.\"?!:_()*' ")
            if IPreprocessor.valid_word(word):
                words.append(word)
        if len(words) == 0:
            return ""
        text = " ".join(words)
        return text

    def apply(self, text: str) -> str:
        return IPreprocessor.word_filter(text)

    @staticmethod
    def valid_word(word: str) -> bool:
        """
        :param word: 输入的单词
        :return: 是否是正常的单词
        """
        if word is None or len(word) == 0:
            return False

        if IPreprocessor.is_cjk(word):
            return True

        """
        hashtag or nickname
        """
        if word.startswith("#") or word.startswith("@"):
            return False

        """
        url
        """
        if word.find("/") >= 0 or word.find(".") >= 0:
            return False

        """
        num or replica char or len(word) == 1
        """
        pre_char = ""
        diff_char = 0
        replica_times = 1
        for word_char in word:
            if word_char.isdigit():
                return False
            if word_char != pre_char:
                replica_times = 1
                diff_char += 1
                pre_char = word_char
            else:
                replica_times += 1
                if replica_times >= 3:
                    return False
        if diff_char == 1:
            return False
        return True


class LatinPreprocessor(IPreprocessor):
    """
    拉丁文
    """

    def __init__(self):
        self._char = []
        self._char.extend(lang_char.french_char)
        self._char.extend(lang_char.spanish_char)
        self._char.extend(lang_char.german_char)
        self._char.extend(lang_char.romanian_char)
        self._char.extend(lang_char.swedish_char)
        self._char.extend(lang_char.polish_char)
        self._char.extend(lang_char.finnish_char)
        self._char.extend(lang_char.hungarian_char)
        self._char.extend(lang_char.lithuanian_char)
        self._char.extend(lang_char.italian_char)
        self._char.extend(lang_char.portuguese_char)

    @property
    def latin_char(self) -> list[str]:
        return self._char

    def apply(self, text: str) -> str:
        text = super(LatinPreprocessor, self).apply(text)
        pre_blank = False
        res = ""
        for word_char in text:
            if word_char in self._char or "a" <= word_char <= "z":
                res += word_char
                pre_blank = False
            else:
                word_char = " "
            if word_char == " " and not pre_blank:
                res += word_char
                pre_blank = True
        return res.strip()


class ArabPreprocessor(IPreprocessor):
    """
    阿语系
    """

    def apply(self, text: str) -> str:
        text = super(ArabPreprocessor, self).apply(text)
        pre_blank = False
        res = ""
        for word_char in text:
            if "\u0600" <= word_char <= "\u06FF" \
                    or "\u0750" <= word_char <= "\u077F" \
                    or "\u08A0" <= word_char <= "\u08FF" \
                    or "\u0001\uEE00" <= word_char <= "\u0001\uEEFF":
                res += word_char
                pre_blank = False
                continue
            if word_char == " " and not pre_blank:
                res += word_char
                pre_blank = True
                continue
            res += " "
            pre_blank = True
        return res.strip()


class CJKPreprocessor(IPreprocessor):
    """
    中日韩
    """

    def apply(self, text: str) -> str:
        res = ""
        for word_char in text:
            if "\u3400" <= word_char <= "\u4DBF" or "\u4E00" <= word_char <= "\u9FFF" \
                    or "\uF900" <= word_char <= "\uFAFF" or "\u3040" <= word_char <= "\u309F" \
                    or "\u30A0" <= word_char <= "\u30FF" or "\u31F0" <= word_char <= "\u31FF":
                res += word_char
                res += " "
        return res.strip()


class RussiaPreprocessor(IPreprocessor):
    """
    俄语系
    """

    def apply(self, text: str) -> str:
        text = super(RussiaPreprocessor, self).apply(text)
        pre_blank = False
        res = ""
        for word_char in text:
            if "\u0410" <= word_char <= "\u044F":
                res += word_char
                pre_blank = False
                continue
            if word_char == " " and not pre_blank:
                res += word_char
                pre_blank = True
                continue
            res += " "
            pre_blank = True
        return res.strip()


if __name__ == '__main__':
    latin_preprocessor = LatinPreprocessor()
    cjh_preprocessor = CJKPreprocessor()
    arab_preprocessor = ArabPreprocessor()
    russian_preprocessor = RussiaPreprocessor()
    latin_corpus = [
        "Étiez vous au courant que l'on pouvait avorter à 9 mois de grossesse en France ?? "
        "Quand à t on consulter les français pour cette mesure abominable ?? Déjà à 14 semaines ça m'a terrifié..."
        "\"Jeder hat das Recht, seine (!) Meinung in Wort, Schrift und Bild frei zu äußern "
        "und zu verbreiten und sich aus allgemein zugänglichen Quellen ungehindert zu unterrichten. "
        "[...] Eine Zensur findet nicht statt.\" (Grundgesetz für die Bundesrepublik Deutschland, Artikel 5, Abs. 1)",
        "Don't forget to say MashAllah🥺♥️Evil eyes off ‼️ #ImamKhadimHussainRizvi #100MostBeautifulFacesOf2022",
        "France plans to deliver VAB armored personnel carriers to Ukraine \"in significant quantities\", "
        "and 6 more Caesar howitzers - 🇫🇷Def Min Sébastien Lecornu",
        "if get to go to france, what do you want to do G: travel O: *points to G* (he's) shopping too ka "
        "G: shopping too, of course/obviously O: oh ok and eat too (i'm not too sure about this part tho)"
    ]
    for line in latin_corpus:
        print(latin_preprocessor.apply(line))

    cjk_corpus = [
        """
        爆裂的鎧甲，迸發的鬥志，超越極限的美鬥士們激情碰撞

與名為「美鬥士」的性感女戰士們一起
探索未知世界的冒險類RPG遊戲
        """,
        """
        欢迎来到美国驻华使领馆的“推特”平台！这里是活动文字直播、思想交流、文化分享的开放平台。本帐号的使用条款可在以下链接找到：http://t.cn/R6HRrV1 有时候，我们的内容会将关注者定向到非美国政府网站，此处包含的链接仅供参考，不一定代表美国政府或美国国务院的观点或背书。关注伯恩斯大使的官方账号: 
@USAmbChina
        """,
        """
        １年前の今日、台湾が新型コロナウイルスとの戦いで多くの困難に直面する中、日本政府からワクチンを贈っていただきました。この時のご厚意は私たちの心に深く刻み込まれています。困難に遭うたびに助け合ってきた台湾と日本の友情は、とても尊いものです。これからも大事にしていきたいと思います。
        """
    ]
    for line in cjk_corpus:
        print(cjh_preprocessor.apply(line))

    russian_corpus = [
        """
        тасс: армия и опк - "открытый партнер": что давать россия преимущество на рынок вооружение индия . квитол (индия), 31 март. /тасс/. деловой программа международный выставка сухопутный и военно-морской вооружение defexpo india - 2016, проходить в южный гоа, завершаться. в этот раз российский экспозиция становиться самый масштабный по количество компания, представлять как новинка, так и уже известный по весь мир образец вооружение и военный техника.о то, какой переговоры проходить с индийский партнер и на что быть сделать основной акцент бизнес-программа, - в специальный материал тасс.   масштабыкак рассказывать заместитель генеральный директор "рособоронэкспорт" сергей гореславский, в этот выставка, несмотря на то, что она проходить в новый место, российский опк впервые за весь история компания принимать участие в такой масштаб: более 60 предприятие и много 500 специалист.по его слово, это отражать то, что индия быть, быть и быть главный стратегический партнер россия по военно-технический сотрудничество (втс).make in indiaнесмотря на иметься перспектива расширение российский присутствие на индийский рынок вооружение, по заявление гореславский, здесь укреплять свой позиция страна, который являться конкурент рф в область втс, но "трагедия из это никто не делать". на вопрос о то, терять ли мы тут рынок, мочь быть только один ответ: нет, мы он не терять. сказать много - быть основание рассчитывать, что присутствие здесь российский технология быть расширятьсясергей гореславскийзаместитель генеральный директор "рособоронэкспорт"гореславский рассказывать, что в ход выставка "рособоронэкспорт" активно поработать с индийский партнер, как с представитель минобороны, включая самый министр, так и с представитель местный крупный компания, по реализация задача, вытекать из программа make in india. он подчеркивать, что россия привлекательный для индия, так как являться наиболее открытый партнер по передача технология.суть программа make in india - привлекать к развитие опк крупный частный капитал и налаживать производство техника на совместный с зарубежный партнер предприятие."рособоронэкспорт" рассматривать местный частный компания как возможный партнер в проект, связывать с укрепление обороноспособность вооруженный сила этот страна. по мнение гореславский, "весь это ставить задача правильный выбор компания, от деятельность который быть зависеть успех проект и его рентабельность"."входить в проект в рамка совместный предприятие - это значить делить ответственность, в тот число и коммерческий, за его будущее", - отмечать он.для то чтобы придавать проект make in india законодательный основа, создавать условие, при который не только частный сектор, но и государство быть брать на себя ответственность, "рособоронэкспорт" предлагать по стратегический проект вести работа на основание межправительственный соглашение.   пилотный проект, отвечать требование этот принцип, являться создание в индия совместный производство вертолет ка-226. в соответствие с межправительственный соглашение, который быть подписывать в декабрь прошлый год, уполномоченная компания от индийский сторона являться государственный компания halсергей гореславскийзаместитель генеральный директор "рособоронэкспорт"но за она, по слово гореславский, сейчас выстраиваться целый цепочка интегратор из сфера частный бизнес, с который "рособоронэкспорт" вести переговоры на выставка.
        """
    ]
    for line in russian_corpus:
        print(russian_preprocessor.apply(line))
