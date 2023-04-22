import json
import discord
from discord.ext import commands
import time
import asyncio
from discord.ext.commands import has_permissions, CheckFailure
import datetime
badwords=['chuj', 'chuja', 'chujek', 'chuju', 'chujem', 'chujnia', 'chujowy', 'chujowa', 'chujowe', 'cipa', 'cipę', 'cipe', 'cipą', 'cipka', 'cipce', 'cipką', 'cipie', 'dojebać', 'dojebac', 'dojebie', 'dojebał', 'dojebal', 'dojebała', 'dojebala', 'dojebałem', 'dojebalem', 'dojebałam', 'dojebalam', 'zjebał', 'dojebał', 'odjebał', 'zjebałem', 'zjebal', 'zjebalem', 'dojebię', 'dojebie', 'dopierdalać', 'dopierdalac', 'dopierdala', 'dopierdalał', 'dopierdalała', 'dopierdalala', 'dopierdoli', 'dopierdolił', 'dopierdolil', 'dopierdolę', 'dopierdole', 'dopierdoli', 'dopierdalający', 'dopierdalajacy', 'dopierdolić', 'dopierdolic', 'huj', 'hujek', 'hujnia', 'huja', 'huje', 'hujem', 'huju', 'jebać', 'jebac', 'jebał', 'jebal', 'jebie', 'jebią', 'jebia', 'jebak', 'jebaka', 'jebal', 'jebał', 'jebany', 'jebane', 'jebanka', 'jebanko', 'jebankiem', 'jebanymi', 'jebana', 'jebanym', 'jebanej', 'jebaną', 'jebana', 'jebani', 'jebanych', 'jebanymi', 'jebcie', 'jebiący', 'jebiacy', 'jebiąca', 'jebiaca', 'jebiącego', 'jebiacego', 'jebiącej', 'jebiacej', 'jebia', 'jebią', 'jebie', 'jebię', 'jebliwy', 'jebnąć', 'jebnac', 'jebnąc', 'jebnać', 'jebnął', 'jebnal', 'jebną', 'jebna', 'jebnęła', 'jebnela', 'jebnie', 'jebnij', 'jebut', 'koorwa', 'kórwa', 'kurestwo', 'kurew', 'kurewski', 'kurewska', 'kurewskiej', 'kurewską', 'kurewska', 'kurewsko', 'kurewstwo', 'kurwa', 'kurwaa', 'kurwami', 'kurwą', 'kurwe', 'kurwę', 'kurwie', 'kurwiska', 'kurwo', 'kurwy', 'kurwach', 'kurwami', 'kurewski', 'kurwiarz', 'kurwiący', 'kurwica', 'kurwić', 'kurwic', 'kurwidołek', 'kurwik', 'kurwiki', 'kurwiszcze', 'kurwiszon', 'kurwiszona', 'kurwiszonem', 'kurwiszony', 'kutas', 'kutasa', 'kutasie', 'kutasem', 'kutasy', 'kutasów', 'kutasow', 'kutasach', 'kutasami', 'matkojebca', 'matkojebcy', 'matkojebcą', 'matkojebca', 'matkojebcami', 'matkojebcach', 'nabarłożyć', 'najebać', 'najebac', 'najebał', 'najebal', 'najebała', 'najebala', 'najebane', 'najebany', 'najebaną', 'najebana', 'najebie', 'najebią', 'najebia', 'naopierdalać', 'naopierdalac', 'napierdalać', 'napierdalac', 'napierdalający', 'napierdalajacy', 'napierdolić', 'napierdolic', 'nawpierdalać', 'nawpierdalac', 'nawpierdalał', 'nawpierdalal', 'nawpierdalała', 'nawpierdalala', 'obsrywać', 'obsrywac', 'obsrywający', 'obsrywajacy', 'odpieprzać', 'odpieprzac', 'odpieprzy', 'odpieprzył', 'odpieprzyl', 'odpieprzyła', 'odpieprzyla', 'odpierdalać', 'odpierdalac', 'odpierdol', 'odpierdolił', 'odpierdolil', 'odpierdoliła', 'odpierdolila', 'odpierdoli', 'odpierdalający', 'odpierdalajacy', 'odpierdalająca', 'odpierdalajaca', 'odpierdolić', 'odpierdolic', 'odpierdoli', 'odpierdolił', 'opieprzający', 'opierdalać', 'opierdalac', 'opierdala', 'opierdalający', 'opierdalajacy', 'opierdol', 'opierdolić', 'opierdolic', 'opierdoli', 'opierdolą', 'opierdola', 'piczka', 'pieprznięty', 'pieprzniety', 'pieprzony', 'pierdel', 'pierdlu', 'pierdolą', 'pierdola', 'pierdolący', 'pierdolacy', 'pierdoląca', 'pierdolaca', 'pierdol', 'pierdole', 'pierdolenie', 'pierdoleniem', 'pierdoleniu', 'pierdolę', 'pierdolec', 'pierdola', 'pierdolą', 'pierdolić', 'pierdolicie', 'pierdolic', 'pierdolił', 'pierdolil', 'pierdoliła', 'pierdolila', 'pierdoli', 'pierdolnięty', 'pierdolniety', 'pierdolisz', 'pierdolnąć', 'pierdolnac', 'pierdolnął', 'pierdolnal', 'pierdolnęła', 'pierdolnela', 'pierdolnie', 'pierdolnięty', 'pierdolnij', 'pierdolnik', 'pierdolona', 'pierdolone', 'pierdolony', 'pierdołki', 'pierdzący', 'pierdzieć', 'pierdziec', 'pizda', 'pizdą', 'pizde', 'pizdę', 'piździe', 'pizdzie', 'pizdnąć', 'pizdnac', 'pizdu', 'podpierdalać', 'podpierdalac', 'podpierdala', 'podpierdalający', 'podpierdalajacy', 'podpierdolić', 'podpierdolic', 'podpierdoli', 'pojeb', 'pojeba', 'pojebami', 'pojebani', 'pojebanego', 'pojebanemu', 'pojebani', 'pojebany', 'pojebanych', 'pojebanym', 'pojebanymi', 'pojebem', 'pojebać', 'pojebac', 'pojebalo', 'popierdala', 'popierdalac', 'popierdalać', 'popierdolić', 'popierdolic', 'popierdoli', 'popierdolonego', 'popierdolonemu', 'popierdolonym', 'popierdolone', 'popierdoleni', 'popierdolony', 'porozpierdalać', 'porozpierdala', 'porozpierdalac', 'poruchac', 'poruchać', 'przejebać', 'przejebane', 'przejebac', 'przyjebali', 'przepierdalać', 'przepierdalac', 'przepierdala', 'przepierdalający', 'przepierdalajacy', 'przepierdalająca', 'przepierdalajaca', 'przepierdolić', 'przepierdolic', 'przyjebać', 'przyjebac', 'przyjebie', 'przyjebała', 'przyjebala', 'przyjebał', 'przyjebal', 'przypieprzać', 'przypieprzac', 'przypieprzający', 'przypieprzajacy', 'przypieprzająca', 'przypieprzajaca', 'przypierdalać', 'przypierdalac', 'przypierdala', 'przypierdoli', 'przypierdalający', 'przypierdalajacy', 'przypierdolić', 'przypierdolic', 'rozjebać', 'rozjebac', 'rozjebie', 'rozjebała', 'rozjebią', 'rozpierdol', 'rozpierdalać', 'rozpierdalac', 'rozpierdala', 'rozpierdolić', 'rozpierdolic', 'rozpierdole', 'rozpierdoli', 'rozpierducha', 'skurwić', 'skurwiel', 'skurwiela', 'skurwielem', 'skurwielu', 'skurwysyn', 'skurwysynów', 'skurwysynow', 'skurwysyna', 'skurwysynem', 'skurwysynu', 'skurwysyny', 'skurwysyński', 'skurwysyńskie', 'skurwysyńsko', 'skurwysynsko', 'skurwysynskieskurwysynski', 'skurwysyństwo', 'skurwysynstwo', 'spieprzać', 'spieprzac', 'spieprza', 'spieprzaj', 'spieprzajcie', 'spieprzają', 'spieprzaja', 'spieprzający', 'spieprzajacy', 'spieprzająca', 'spieprzajaca', 'spierdalać', 'spierdalac', 'spierdala', 'spierdalał', 'spierdalała', 'spierdalal', 'spierdalalcie', 'spierdalala', 'spierdalający', 'spierdalajacy', 'spierdolić', 'spierdolic', 'spierdoli', 'spierdoliła', 'spierdoliło', 'spierdolą', 'spierdola', 'sukinsyn', 'sukinsyny', 'sukinsynom', 'sukinsynowi', 'sukinsynów', 'sukinsynow', 'ujebać', 'ujebac', 'ujebał', 'ujebal', 'ujebana', 'ujebany', 'ujebie', 'ujebała', 'ujebala', 'upierdalać', 'upierdalac', 'upierdala', 'upierdoli', 'upierdolić', 'upierdolic', 'upierdoli', 'upierdolą', 'upierdola', 'upierdoleni', 'wjebać', 'wjebac', 'wjebie', 'wjebią', 'wjebia', 'wjebiemy', 'wjebiecie', 'wkurwiać', 'wkurwiac', 'wkurwi', 'wkurwia', 'wkurwiał', 'wkurwial', 'wkurwiający', 'wkurwiajacy', 'wkurwiająca', 'wkurwiajaca', 'wkurwić', 'wkurwic', 'wkurwi', 'wkurwiacie', 'wkurwiają', 'wkurwiali', 'wkurwią', 'wkurwia', 'wkurwimy', 'wkurwicie', 'wkurwiacie', 'wkurwić', 'wkurwic', 'wkurwia', 'wpierdalać', 'wpierdalac', 'wpierdalający', 'wpierdalajacy', 'wpierdol', 'wpierdolić', 'wpierdolic', 'wpizdu', 'wyjebać', 'wyjebac', 'wyjebali', 'wyjebał', 'wyjebac', 'wyjebała', 'wyjebały', 'wyjebie', 'wyjebią', 'wyjebia', 'wyjebiesz', 'wyjebie', 'wyjebiecie', 'wyjebiemy', 'wypieprzać', 'wypieprzac', 'wypieprza', 'wypieprzał', 'wypieprzal', 'wypieprzała', 'wypieprzala', 'wypieprzy', 'wypieprzyła', 'wypieprzyla', 'wypieprzył', 'wypieprzyl', 'wypierdal', 'wypierdalać', 'wypierdalac', 'wypierdala', 'wypierdalaj', 'wypierdalania', 'wypierdalał', 'wypierdalal', 'wypierdalała', 'wypierdalala', 'wypierdalać', 'wypierdolić', 'wypierdolic', 'wypierdoli', 'wypierdolimy', 'wypierdolicie', 'wypierdolą', 'wypierdola', 'wypierdolili', 'wypierdolił', 'wypierdolil', 'wypierdoliła', 'wypierdolila', 'zajebać', 'zajebac', 'zajebie', 'zajebią', 'zajebia', 'zajebiał', 'zajebial', 'zajebała', 'zajebiala', 'zajebali', 'zajebana', 'zajebani', 'zajebane', 'zajebany', 'zajebanych', 'zajebanym', 'zajebanymi', 'zapierdala', 'zapierdalać', 'zapierdalac', 'zapierdalaja', 'zapierdalał', 'zapierdalaj', 'zapierdalajcie', 'zapierdalała', 'zapierdalala', 'zapierdalali', 'zapierdalający', 'zapierdalajacy', 'zapierdolić', 'zapierdolic', 'zapierdoli', 'zapierdolić', 'zapierdolil', 'zapierdoliła', 'zapierdolila', 'zapierdolą', 'zapierdola', 'zapierniczać', 'zapierniczający', 'zjebać', 'zjebac', 'zjebał', 'zjebal', 'zjebała', 'zjebala', 'zjebana', 'zjebią', 'zjebali', 'zjeby', 'cipa', 'kurwy','nigga','penis','chuj', 'chuja', 'chujek', 'chujem', 'chujnia', 'chujowa', 'chujowe', 'chujowy', 'chuju', 'ciot', 'ciota', 'cip', 'cipa', 'cipach', 'cipami', 'cipce', 'cipe', 'cipek', 'cipie', 'cipka', 'cipkach', 'cipkami', 'cipki', 'cipko', 'cipkom', 'cipką', 'cipkę', 'cipo', 'cipom', 'cipy', 'cipą', 'cipę', 'ciul', 'debilu', 'dojebac', 'dojebal', 'dojebala', 'dojebalam', 'dojebalem', 'dojebać', 'dojebał', 'dojebała', 'dojebałam', 'dojebałem', 'dojebie', 'dojebię', 'dopieprzac', 'dopieprzać', 'dopierdala', 'dopierdalac', 'dopierdalajacy', 'dopierdalający', 'dopierdalal', 'dopierdalala', 'dopierdalać', 'dopierdalał', 'dopierdalała', 'dopierdole', 'dopierdoli', 'dopierdolic', 'dopierdolil', 'dopierdolić', 'dopierdolił', 'dopierdolę', 'dupie','downie', 'dzifka', 'dzifko', 'dziwka', 'dziwko', 'fiucie', 'fiut', 'fuck', 'huj', 'huja', 'huje', 'hujek', 'hujem', 'hujnia', 'huju', 'hój', 'jebac', 'jebak', 'jebaka', 'jebako', 'jebal', 'jebana', 'jebane', 'jebanej', 'jebani', 'jebanka', 'jebankiem', 'jebanko', 'jebany', 'jebanych', 'jebanym', 'jebanymi', 'jebaną', 'jebać', 'jebał', 'jebcie', 'jebia', 'jebiaca', 'jebiacego', 'jebiacej', 'jebiacy', 'jebie', 'jebią', 'jebiąca', 'jebiącego', 'jebiącej', 'jebiący', 'jebię', 'jebliwy', 'jebna', 'jebnac', 'jebnal', 'jebnać', 'jebnela', 'jebnie', 'jebnij', 'jebną', 'jebnąc', 'jebnąć', 'jebnął', 'jebnęła', 'jebut', 'koorwa', 'korewko', 'kurestwo', 'kurew', 'kurewko', 'kurewska', 'kurewski', 'kurewskiej', 'kurewsko', 'kurewską', 'kurewstwo', 'kurwa', 'kurwaa', 'kurwach', 'kurwami', 'kurwe', 'kurwiarz', 'kurwic', 'kurwica', 'kurwidołek', 'kurwie', 'kurwik', 'kurwiki', 'kurwiska', 'kurwiszcze', 'kurwiszon', 'kurwiszona', 'kurwiszonem', 'kurwiszony', 'kurwiący', 'kurwić', 'kurwo', 'kurwy', 'kurwą', 'kurwę', 'kutas', 'kutasa', 'kutasach', 'kutasami', 'kutasem', 'kutasie', 'kutasow', 'kutasy', 'kutasów', 'kórewko', 'kórwa', 'lesbijko', 'matkojebca', 'matkojebcach', 'matkojebcami', 'matkojebcy', 'matkojebcą', 'morde', 'mordę', 'nabarłożyć', 'najebac', 'najebal', 'najebala', 'najebana', 'najebane', 'najebany', 'najebaną', 'najebać', 'najebał', 'najebała', 'najebia', 'najebie', 'najebią', 'nakurwiac', 'nakurwiamy', 'nakurwiać', 'nakurwiscie', 'nakurwiście', 'naopierdalac', 'naopierdalal', 'naopierdalala', 'naopierdalać', 'naopierdalał', 'naopierdalała', 'napierdalac', 'napierdalajacy', 'napierdalający', 'napierdalać', 'napierdolic', 'napierdolić', 'nawpierdalac', 'nawpierdalal', 'nawpierdalala', 'nawpierdalać', 'nawpierdalał', 'nawpierdalała', 'obsrywac', 'obsrywajacy', 'obsrywający', 'obsrywać', 'odpieprzac', 'odpieprzać', 'odpieprzy', 'odpieprzyl', 'odpieprzyla', 'odpieprzył', 'odpieprzyła', 'odpierdalac', 'odpierdalajaca', 'odpierdalajacy', 'odpierdalająca', 'odpierdalający', 'odpierdalać', 'odpierdol', 'odpierdoli', 'odpierdolic', 'odpierdolil', 'odpierdolila', 'odpierdolić', 'odpierdolił', 'odpierdoliła', 'opieprzający', 'opierdala', 'opierdalac', 'opierdalajacy', 'opierdalający', 'opierdalać', 'opierdol', 'opierdola', 'opierdoli', 'opierdolic', 'opierdolić', 'opierdolą', 'pedale', 'picza', 'piczka', 'piczo', 'pieprz', 'pieprzniety', 'pieprznięty', 'pieprzony', 'pierdel', 'pierdlu', 'pierdol', 'pierdola', 'pierdolaca', 'pierdolacy', 'pierdole', 'pierdolec', 'pierdolenie', 'pierdoleniem', 'pierdoleniu', 'pierdoli', 'pierdolic', 'pierdolicie', 'pierdolil', 'pierdolila', 'pierdolisz', 'pierdolić', 'pierdolił', 'pierdoliła', 'pierdolnac', 'pierdolnal', 'pierdolnela', 'pierdolnie', 'pierdolniety', 'pierdolnij', 'pierdolnik', 'pierdolnięty', 'pierdolny', 'pierdolnąć', 'pierdolnął', 'pierdolnęła', 'pierdolona', 'pierdolone', 'pierdolony', 'pierdolą', 'pierdoląca', 'pierdolący', 'pierdolę', 'pierdołki', 'pierdziec', 'pierdzieć', 'pierdzący', 'pizda', 'pizde', 'pizdnac', 'pizdnąć', 'pizdu', 'pizdzie', 'pizdą', 'pizdę', 'piździe', 'podjebac', 'podjebać', 'podkurwic', 'podkurwić', 'podpierdala', 'podpierdalac', 'podpierdalajacy', 'podpierdalający', 'podpierdalać', 'podpierdoli', 'podpierdolic', 'podpierdolić', 'pojeb', 'pojeba', 'pojebac', 'pojebalo', 'pojebami', 'pojebancu', 'pojebane', 'pojebanego', 'pojebanemu', 'pojebani', 'pojebany', 'pojebanych', 'pojebanym', 'pojebanymi', 'pojebać', 'pojebańcu', 'pojebem', 'popierdala', 'popierdalac', 'popierdalać', 'popierdolencu', 'popierdoleni', 'popierdoleńcu', 'popierdoli', 'popierdolic', 'popierdolić', 'popierdolone', 'popierdolonego', 'popierdolonemu', 'popierdolony', 'popierdolonym', 'porozpierdala', 'porozpierdalac', 'porozpierdalać', 'poruchac', 'poruchać', 'przejebac', 'przejebane', 'przejebać', 'przepierdala', 'przepierdalac', 'przepierdalajaca', 'przepierdalajacy', 'przepierdalająca', 'przepierdalający', 'przepierdalać', 'przepierdolic', 'przepierdolić', 'przyjebac', 'przyjebal', 'przyjebala', 'przyjebali', 'przyjebać', 'przyjebał', 'przyjebała', 'przyjebie', 'przypieprzac', 'przypieprzajaca', 'przypieprzajacy', 'przypieprzająca', 'przypieprzający', 'przypieprzać', 'przypierdala', 'przypierdalac', 'przypierdalajacy', 'przypierdalający', 'przypierdalać', 'przypierdoli', 'przypierdolic', 'przypierdolić', 'qrwa', 'rozjeb', 'rozjebac', 'rozjebali', 'rozjebaliście', 'rozjebaliśmy', 'rozjebać', 'rozjebał', 'rozjebała', 'rozjebałam', 'rozjebałaś', 'rozjebałem', 'rozjebałeś', 'rozjebało', 'rozjebały', 'rozjebałyście', 'rozjebałyśmy', 'rozjebcie', 'rozjebie', 'rozjebiecie', 'rozjebiemy', 'rozjebiesz', 'rozjebią', 'rozjebię', 'rozjebmy', 'rozpierdala', 'rozpierdalac', 'rozpierdalać', 'rozpierdole', 'rozpierdoli', 'rozpierdolic', 'rozpierdolić', 'rozpierducha', 'rucha', 'ruchacie', 'ruchaj', 'ruchajcie', 'ruchajmy', 'ruchają', 'ruchali', 'ruchaliście', 'ruchaliśmy', 'rucham', 'ruchamy', 'ruchasz', 'ruchać', 'ruchał', 'ruchała', 'ruchałam', 'ruchałaś', 'ruchałem', 'ruchałeś', 'ruchało', 'ruchałom', 'ruchałoś', 'ruchały', 'ruchałyście', 'ruchałyśmy', 'ryj', 'skurwic', 'skurwiel', 'skurwiela', 'skurwielem', 'skurwielu', 'skurwić', 'skurwysyn', 'skurwysyna', 'skurwysynem', 'skurwysynow', 'skurwysynski', 'skurwysynstwo', 'skurwysynu', 'skurwysyny', 'skurwysynów', 'skurwysyński', 'skurwysyństwo', 'skutasiony', 'spermosiorbacz', 'spermosiorbaczem', 'spieprza', 'spieprzac', 'spieprzaj', 'spieprzaja', 'spieprzajaca', 'spieprzajacy', 'spieprzajcie', 'spieprzają', 'spieprzająca', 'spieprzający', 'spieprzać', 'spierdala', 'spierdalac', 'spierdalaj', 'spierdalajacy', 'spierdalający', 'spierdalal', 'spierdalala', 'spierdalalcie', 'spierdalać', 'spierdalał', 'spierdalała', 'spierdola', 'spierdolencu', 'spierdoleńcu', 'spierdoli', 'spierdolic', 'spierdolić', 'spierdoliła', 'spierdoliło', 'spierdolą', 'srac', 'sraj', 'srajac', 'srajacy', 'srając', 'srający', 'srać', 'sukinsyn', 'sukinsynom', 'sukinsynow', 'sukinsynowi', 'sukinsyny', 'sukinsynów', 'szmata', 'szmato', 'udupić', 'ujebac', 'ujebal', 'ujebala', 'ujebana', 'ujebany', 'ujebać', 'ujebał', 'ujebała', 'ujebie', 'upierdala', 'upierdalac', 'upierdalać', 'upierdol', 'upierdola', 'upierdoleni', 'upierdoli', 'upierdolic', 'upierdolić', 'upierdolą', 'wjebac', 'wjebać', 'wjebia', 'wjebie', 'wjebiecie', 'wjebiemy', 'wjebią', 'wkurwi', 'wkurwia', 'wkurwiac', 'wkurwiacie', 'wkurwiajaca', 'wkurwiajacy', 'wkurwiają', 'wkurwiająca', 'wkurwiający', 'wkurwial', 'wkurwiali', 'wkurwiać', 'wkurwiał', 'wkurwic', 'wkurwicie', 'wkurwimy', 'wkurwią', 'wkurwić', 'wpierdalac', 'wpierdalajacy', 'wpierdalający', 'wpierdalać', 'wpierdol', 'wpierdolic', 'wpierdolić', 'wpizdu', 'wyjebac', 'wyjebali', 'wyjebany', 'wyjebać', 'wyjebał', 'wyjebała', 'wyjebały', 'wyjebia', 'wyjebie', 'wyjebiecie', 'wyjebiemy', 'wyjebiesz', 'wyjebią', 'wykurwic', 'wykurwić', 'wykurwiście', 'wypieprza', 'wypieprzac', 'wypieprzal', 'wypieprzala', 'wypieprzać', 'wypieprzał', 'wypieprzała', 'wypieprzy', 'wypieprzyl', 'wypieprzyla', 'wypieprzył', 'wypieprzyła', 'wypierdal', 'wypierdala', 'wypierdalac', 'wypierdalaj', 'wypierdalal', 'wypierdalala', 'wypierdalać', 'wypierdalał', 'wypierdalała', 'wypierdola', 'wypierdoli', 'wypierdolic', 'wypierdolicie', 'wypierdolil', 'wypierdolila', 'wypierdolili', 'wypierdolimy', 'wypierdolić', 'wypierdolił', 'wypierdoliła', 'wypierdolą', 'wypiździały', 'zajebac', 'zajebali', 'zajebana', 'zajebane', 'zajebani', 'zajebany', 'zajebanych', 'zajebanym', 'zajebanymi', 'zajebać', 'zajebała', 'zajebia', 'zajebial', 'zajebiala', 'zajebiał', 'zajebie', 'zajebiscie', 'zajebista', 'zajebiste', 'zajebisty', 'zajebistych', 'zajebistym', 'zajebistymi', 'zajebią', 'zajebiście', 'zapieprza', 'zapieprzy', 'zapieprzyc', 'zapieprzycie', 'zapieprzyl', 'zapieprzyla', 'zapieprzymy', 'zapieprzysz', 'zapieprzyć', 'zapieprzył', 'zapieprzyła', 'zapieprzą', 'zapierdala', 'zapierdalac', 'zapierdalaj', 'zapierdalaja', 'zapierdalajacy', 'zapierdalajcie', 'zapierdalający', 'zapierdalala', 'zapierdalali', 'zapierdalać', 'zapierdalał', 'zapierdalała', 'zapierdola', 'zapierdoli', 'zapierdolic', 'zapierdolil', 'zapierdolila', 'zapierdolić', 'zapierdolił', 'zapierdoliła', 'zapierdolą', 'zapierniczający', 'zapierniczać', 'zasranym', 'zasrać', 'zasrywający', 'zasrywać', 'zesrywający', 'zesrywać', 'zjebac', 'zjebal', 'zjebala', 'zjebali', 'zjebana', 'zjebancu', 'zjebane', 'zjebać', 'zjebał', 'zjebała', 'zjebańcu', 'zjebią', 'zjeby', 'śmierdziel','nigg']
admins_role_id=0
id_serwa=0
TOKEN=""
intents=discord.Intents.all()
discord.member = True
intents.message_content = True
bot = discord.Client( intents=intents, case_insensitive=True)
tree = discord.app_commands.CommandTree(bot)
plik = open("databaseClock.json","r")
databaseClock = json.loads(plik.read())
plik.close()
plik = open("database.json","r")
database = json.loads(plik.read())
plik.close()
async def check(member):
    for i in database:
        if i.get("name")==member.id:
            if i.get("points")>=15 and i.get("warnings")==None:
                await member.send("Przekroczono limit punktów karnych (1 ostrzeżenie)")
                await member.kick(reason="Punkty karne (1)")
                i["points"]=0
                i["warnings"]=1
                save()
            if i.get("points")>=15 and i.get("warnings")>=1:
                i["warnings"]+=1
                if i.get("warnings")<=3:
                    await member.send("Przekroczono limit punktów karnych ("+str(i.get("warnings"))+" ostrzeżenie)")
                    await member.kick(reason="Punkty karne ("+str(i.get("warnings"))+" ostrzeżeń)")
                    i["points"]=0
                    save()
                elif i.get("warnings")>=4:
                    await member.send("Przekroczono limit punktów karnych przez co otrzymałeś bana. Skontaktuj się z administracją (RooiGevaar19#9997) aby zyskać możliwego unbana.")
                    await member.ban(reason="Punkty karne (x>=4 ostrzeżeń)")
                    i["points"]=0
                    i["warnings"]=0
                save()
async def resetPoints():
    plik = open("time.json","r")
    time = int(plik.read())
    plik.close()
    while True:
        time-=1
        save()
        await asyncio.sleep(1)
        for user in databaseClock:
            if user.get("timeToKick")<=0:
                czy_isnieje=False
                for i in database:
                    if i.get("name")==user.get("userId"):
                        i["points"]=15
                        czy_isnieje=True
                if czy_isnieje==False:
                    database.append({"name":user.get("userId"),"points":15})
                save()
                
                guildDoClock = bot.get_guild(id_serwa)
                member = guildDoClock.get_member(user.get("userId"))
                await member.send("Zostałeś wyrzucony za bardzo małą aktywność na serwerze.")
                await check(member) 
                databaseClock.remove({"userId":user.get("userId"),"timeToKick":user.get("timeToKick")})
            else:   
                user["timeToKick"]-=1
        plik = open("databaseClock.json","w+")
        plik.write(json.dumps(databaseClock))
        plik.close()
        if time <=0:
            for i in database:
                if i.get("points")>0:
                    i["points"]-=1
            time=10800

        plik = open("time.json","w+")
        plik.write(str(time))
        plik.close()
def load():
    global database
    try:
        plik = open("database.json","r")
    except:
        plik = open("database.json","w")
        plik.write("[]")
        plik.close()
        database = []
        print("Restarted database! \n")
    try:
        database = json.loads(plik.read())
    except:
        plik.close()
        plik = open("database.json","a")
        plik.write("[]")
        plik.close()
        load()
    plik.close()
def save():
    plik = open("database.json","w+")
    plik.write(json.dumps(database))
    plik.close()
@bot.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=id_serwa))
    print("I'm ready!")
    await resetPoints()
@bot.event
async def on_member_join(member):
    if time.time() - member.created_at.timestamp() < 7_890_000 : #3 miesiące w sekundach
        await member.send("Twoje konto zostało uznane za skrajnie podejrzane. Spróbuj ponownie kiedy indziej :)")
        await member.kick(reason="Fresh account")
    for i in badwords:
        if i in member.display_name.lower():
            await member.send("Twój nick jest zbyt wulgarny. Zmień nick i przyjdź ponownie :)")
            await member.kick(reason="Wulgarny nick")
    databaseClock.append({"userId":member.id,"timeToKick":7_890_000})
    plik = open("databaseClock.json","w+")
    plik.write(json.dumps(databaseClock))
    plik.close()
@bot.event
async def on_member_update(before, after):
    for i in badwords:
        if i in after.nick.lower():
            await after.edit(nick=before.nick)
            await after.send("Twój nick jest zbyt wulgarny. Został automatycznie zresetowany. Nie zmieniaj go ponownie na taki (+ 5 punktów karnych)")
            czy_isnieje=False
            for i in database:
                if i.get("name")==after.id:
                    i["points"]+=3
                    czy_isnieje=True
            if czy_isnieje==False:
                database.append({"name":after.id,"points":3})
            save()
            await check(after)
@bot.event
async def on_member_leave(member):
    for user in databaseClock:
        try:
            if user.get("userId") == member.id:
                databaseClock.remove({"userId":user.get("userId"),"timeToKick":user.get("timeToKick")})
        except:
            pass
@bot.event
async def on_member_ban(guild, member):
    plik = open("bans.json","r")
    bans = json.loads(plik.read())
    plik.close()
    banned_reason=None
    async for entry in guild.bans(limit=10):
        if entry.user.id == member.id:
            banned_reason=entry.reason
    bans.append({"dateBan":str(datetime.datetime.now()),"id":str(member.id),"reason":str(banned_reason),"caughtNick":str(member),"accCreated":str(member.created_at.astimezone()),"joinServer":str(member.joined_at.astimezone())})
    plik = open("bans.json","w+")
    plik.write(json.dumps(bans))
    plik.close()
@bot.event
async def on_message(message):
    for i in databaseClock:
        if message.author.id == i.get("userId"):
                i["timeToKick"]=7_890_000
    if message.content.lower() == "siema":
        await message.channel.send("No siema :)", reference=message)
    word=""
    dlugosc = message.content
    dlugoscZbadana = 0
    for i in message.content:
        if i in [" ","!","#","%","^","*","(",")","-","+","_","=","~","`","[","]","{","}",";",":","'",'"',"|",'\\',",","<",".",">","/","?"]:
            dlugoscZbadana+=1
            if word in badwords: 
                await message.delete()
                await message.channel.send(f"{message.author.mention} nieładnie tak brzydko mówić (+3 punkty karne) :(")
                czy_isnieje=False
                for i in database:
                    if i.get("name")==message.author.id:
                        i["points"]+=3
                        czy_isnieje=True
                if czy_isnieje==False:
                    database.append({"name":message.author.id,"points":3})
                save()
                await check(message.author)
               	for i in database:
                    if i.get("name")==message.author.id:
                        if i.get("warnings")==None:
                            warnings=0
                        else:
                            warnings=i.get("warnings")
                        embed = discord.Embed(
                        colour=discord.Colour.red(),
                        title=f"Twoja kartoteka obecnie:")
                        embed.add_field(name="Punkty:", value=str(i.get('points')))
                        embed.add_field(name="Ostrzeżenia:", value=str(warnings))
                        await message.channel.send(embed=embed)
            word=""
        else:
            if i == "@":
                word+="a"
            elif i=="$":
                word+="s"
            elif i=="&":
                word+="i"
            else:
                word+= i.lower()
            dlugoscZbadana+=1
        if dlugoscZbadana>=len(message.content):
            if word in badwords: 
                await message.delete()
                await message.channel.send(f"{message.author.mention} nieładnie tak brzydko mówić (+3 punkty karne) :(")
                czy_isnieje=False
                for i in database:
                    if i.get("name")==message.author.id:
                        i["points"]+=3
                        czy_isnieje=True
                if czy_isnieje==False:
                    database.append({"name":message.author.id,"points":3})
                word=""
                save()
                await check(message.author)
               	for i in database:
                    if i.get("name")==message.author.id:
                        if i.get("warnings")==None:
                            warnings=0
                        else:
                            warnings=i.get("warnings")
                        embed = discord.Embed(
                        colour=discord.Colour.red(),
                        title=f"Twoja kartoteka obecnie:")
                        embed.add_field(name="Punkty:", value=str(i.get('points')))
                        embed.add_field(name="Ostrzeżenia:", value=str(warnings))
                        await message.channel.send(embed=embed)
		    
@bot.event
async def on_message_edit(before, after):
    word=""
    dlugosc = after.content
    dlugoscZbadana = 0
    for i in after.content:
        if i in [" ","!","#","%","^","*","(",")","-","+","_","=","~","`","[","]","{","}",";",":","'",'"',"|",'\\',",","<",".",">","/","?"]:
            dlugoscZbadana+=1
            if word in badwords: 
                await after.delete()
                await after.channel.send(f"{after.author.mention} nieładnie tak brzydko mówić (+3 punkty karne) :(")
                czy_isnieje=False
                for i in database:
                    if i.get("name")==after.author.id:
                        i["points"]+=3
                        czy_isnieje=True
                if czy_isnieje==False:
                    database.append({"name":after.author.id,"points":3})
                
                save()
                await check(after.author)
                for i in database:
                    if i.get("name")==after.author.id:
                        if i.get("warnings")==None:
                            warnings=0
                        else:
                            warnings=i.get("warnings")
                        embed = discord.Embed(
                        colour=discord.Colour.red(),
                        title=f"Twoja kartoteka obecnie:")
                        embed.add_field(name="Punkty:", value=str(i.get('points')))
                        embed.add_field(name="Ostrzeżenia:", value=str(warnings))
                        await after.channel.send(embed=embed)
            word=""
        else:
            if i == "@":
                word+="a"
            elif i=="$":
                word+="s"
            elif i=="&":
                word+="i"
            else:
                word+= i.lower()
            dlugoscZbadana+=1
        if dlugoscZbadana>=len(after.content):
            if word in badwords: 
                await after.delete()
                await after.channel.send(f"{after.author.mention} nieładnie tak brzydko mówić (+3 punkty karne) :(")
                czy_isnieje=False
                for i in database:
                    if i.get("name")==after.author.id:
                        i["points"]+=3
                        czy_isnieje=True
                if czy_isnieje==False:
                    database.append({"name":after.author.id,"points":3})
                save()
                await check(after.author)
                word=""
                for i in database:
                    if i.get("name")==after.author.id:
                        if i.get("warnings")==None:
                            warnings=0
                        else:
                            warnings=i.get("warnings")
                        embed = discord.Embed(
                        colour=discord.Colour.red(),
                        title=f"Twoja kartoteka obecnie:")
                        embed.add_field(name="Punkty:", value=str(i.get('points')))
                        embed.add_field(name="Ostrzeżenia:", value=str(warnings))
                        await after.channel.send(embed=embed)
@tree.command(name = "clear", description = "Usuń dowolną liczbę wiadomości (uważaj bo nie ma hamulców)", guild=discord.Object(id=id_serwa)) 
@discord.app_commands.checks.has_role(admins_role_id)
async def clear(interaction: discord.Interaction, amount: int):
    await interaction.response.defer()
    channel = interaction.channel
    await channel.purge(limit=amount+1)
    await interaction.channel.send(f"Usunięto {amount} wiadomości, pani/panie {interaction.user.mention}")
@clear.error
async def error_clear(interaction, x):
    await interaction.response.send_message(f"(/clear) Brak uprawnień, {interaction.user.mention}")
@tree.command(name = "kartoteka", description = "Sprawdź swoją kartotekę", guild=discord.Object(id=id_serwa)) 
async def kartoteka(interaction: discord.Interaction):
    wykrocz=False
    for i in database:
        if i.get("name")==interaction.user.id:
            if i.get("warnings")==None:
                warnings=0
            else:
                warnings=i.get("warnings")
            embed = discord.Embed(
            colour=discord.Colour.red(),
            title=f"Twoja kartoteka {interaction.user.name}:")
            embed.add_field(name="Punkty:", value=str(i.get('points')))
            embed.add_field(name="Ostrzeżenia:", value=str(warnings))
            embed.add_field(name="Przypominamy", value="Za każde 15 punktów otrzymujesz ostrzeżenie i zostajesz wyrzucony z serwera (twoje punkty się zerują także przy tym). Każdy otrzymuje maksymalnie 3 otrzeżenia. Gdy po raz czwarty uzbiera ci się 15 punktów, zostajesz zbanowany i pozostaje ci się odwołać u moderatora czy admina.", inline=False)
            await interaction.response.send_message(embed=embed)
            wykrocz=True
    if wykrocz==False:
        await interaction.response.send_message(f"{interaction.user.mention}, nie posiadasz żadnych wykroczeń i nie byłeś nigdy notowany.")
@tree.command(name = "księga-wykroczeń", description = "Sprawdź czyjąś bibliotekę", guild=discord.Object(id=id_serwa)) 
@discord.app_commands.checks.has_role(admins_role_id)
async def ksiega(interaction: discord.Interaction, uzytkownik: discord.Member):
    wykrocz=False
    for i in database:
        if i.get("name")==uzytkownik.id:
            if i.get("warnings")==None:
                warnings=0
            else:
                warnings=i.get("warnings")
            embed = discord.Embed(
            colour=discord.Colour.red(),
            title=f"Kartoteka użytkonika {uzytkownik.name}:")
            embed.add_field(name="Punkty:", value=str(i.get('points')))
            embed.add_field(name="Ostrzeżenia:", value=str(warnings))
            embed.add_field(name="Przypominamy", value="Za każde 15 punktów otrzymujesz ostrzeżenie i zostajesz wyrzucony z serwera (twoje punkty się zerują także przy tym). Każdy otrzymuje maksymalnie 3 otrzeżenia. Gdy po raz czwarty uzbiera ci się 15 punktów, zostajesz zbanowany i pozostaje ci się odwołać u moderatora czy admina.", inline=False)
            await interaction.response.send_message(embed=embed)
            wykrocz=True
    if wykrocz==False:
        await interaction.response.send_message(f"{uzytkownik.mention}, nie posiada żadnych wykroczeń i nie był nigdy notowany.")
@ksiega.error
async def error_ksiega(interaction, x):
    channel = interaction.channel
    await interaction.response.send_message(f"(/księga-wykroczeń) Brak uprawnień, {interaction.user.mention}")
load()
bot.run(TOKEN)
