SELECT
    T0.[DocNum] as 'Nº documento',
    MAX(T1.[ShipDate]) as 'Data de entrega',
    T0.[DocDate] as 'Data do documento',
    T0.[CardName] as 'Cliente',
    X9.[Usage] as [Utilização],
    SUM(TK.[RelQtty]) as 'Total em ctos',
    CASE WHEN  X9.[Usage] = 'S-Rem a Ordem Futura' THEN 0
		 WHEN  T0.GroupNum = '40' THEN 0
        ELSE SUM(ISNULL(T1.Price, 0) * (ISNULL(TK.[RelQtty], 0) / ISNULL(T1.NumPerMsr, 1)))
    END as 'Total sem imposto',

	CASE WHEN  X9.[Usage] = 'S-Rem a Ordem Futura' THEN 0
				 WHEN  T0.GroupNum = '40' THEN 0
        ELSE SUM((((T1.Price * (TK.[RelQtty] / ISNULL(T1.NumPerMsr, 1))) * T1.LineVat) / t1.LineTotal) + (T1.Price * (TK.[RelQtty] / ISNULL(T1.NumPerMsr, 1))))
    END as 'Total com imposto',
	
	isnull(T3.GrsAmount,0) as 'Frete',
	CASE WHEN  X9.[Usage] = 'S-Rem a Ordem Futura' THEN 0
		 WHEN  T0.GroupNum = '40' THEN 0
		WHEN T3.GrsAmount IS NULL THEN SUM((((T1.Price * (TK.[RelQtty] / ISNULL(T1.NumPerMsr, 1))) * T1.LineVat) / t1.LineTotal) + (T1.Price * (TK.[RelQtty] / ISNULL(T1.NumPerMsr, 1))))
        ELSE SUM((((isnull(T1.Price,0) * (isnull(TK.[RelQtty],0) / ISNULL(T1.NumPerMsr, 1))) * isnull(T1.LineVat,0)) / isnull(t1.LineTotal,0)) + (isnull(T1.Price,0) * (isnull(TK.[RelQtty],0) / ISNULL(T1.NumPerMsr, 1)))) + isnull(T3.GrsAmount,0)
    END as 'Total com frete incluso'
FROM
    ORDR T0
INNER JOIN RDR1 T1 ON T0.[DocEntry] = T1.[DocEntry]
INNER JOIN PKL1 TK ON Tk.OrderEntry = t0.DocEntry AND TK.OrderLine = T1.LineNum 
	---T1.[PickIdNo] = TK.[AbsEntry] AND TK.OrderLine = T1.LineNum
INNER JOIN OPKL TK1 ON TK1.AbsEntry = Tk.AbsEntry
LEFT JOIN RDR3 T3 ON T3.DocEntry = T0.DocEntry -- T3.BaseRef = T1.BaseRef
LEFT JOIN OUSG X9 ON X9.[ID] = T1.[Usage]


WHERE
    T1.PickIdNo IS NOT NULL
    AND T1.[ShipDate] BETWEEN DATEADD(MONTH, -6, GETDATE()) AND GETDATE()
    AND T1.PickStatus IN ('R', 'Y')
    AND TK.[RelQtty] <> 0
GROUP BY
    T0.[DocNum], T0.[DocDate], T0.[CardName], T0.GroupNum, T3.GrsAmount, X9.[Usage]--, Tk1.AbsEntry"""

