#!/usr/bin/env python

from math import *
import copy

class TableDisplayer:
	cols=list()
	rows=list()

        def __init__(self,cols,rows):
            self.cols=cols
            self.rows=rows

	def format(self,t):
		if len(self.rows)==0:
			return ''

		return {
			'text': self.to_text(),
			'html':	self.to_html(),
			'json': self.to_json()			
		}[t]

	def to_text(self):
		HEAD_STYLE='-'

                #make a copy
                cols=list(self.cols)
                rows=copy.deepcopy(self.rows)

		col_num=len(cols)
		row_num=len(rows)
		tmplst=list(rows)
		has_header=False
		# if cols is defined, them merge it into the list
		if col_num!=0:
			has_header=True
			tmplst.insert(0,cols)
		elif len(rows)>0:
			col_num=len(rows[0])

		col_wids=list()
		# calculate the max width for each column
		for i in range(0,col_num):
			max_len=0		
			for row in tmplst:
				col=str(row[i])
				col_len=len(col)
				if col_len>max_len:
					max_len=col_len
			if i!=col_num-1:
				if max_len/8 == 1:
					max_len=max_len+8
				else:
					max_len=int(ceil(max_len/8.0)*8)		
			col_wids.append(max_len)
		
		final_str=''
		head_str=''
		body_str=''
		# add the seperator if header is define
		if has_header:
			total_width=sum(col_wids)
			line=''.join([HEAD_STYLE for num in range(1,total_width)])+'\n'
			head_str=line+self.form_row(cols,col_wids)+line

		# return the table text
		for row in rows:
			row_str=self.form_row(row,col_wids)
			body_str+=row_str

		final_str=head_str+body_str
		return final_str						

	def form_row(self,row,col_wids):
		for i in range(0,len(row)):
			row[i]=str(row[i]).ljust(col_wids[i],' ')	
		row.append('\n')
		row_str=''.join(row)
		return row_str

	def to_html(self):
            #make a copy
            cols=copy.copy(self.cols)
            rows=copy.deepcopy(self.rows)
            thead=''
            if len(cols)!=0:
                theadlist=list('<tr bgcolor=yellow>')
                for col in cols:
                    theadlist.append('<td>'+col+'</td>')
                theadlist.append('</tr>')
                thead=''.join(theadlist)

            tbodylist=list()    
            for row in rows:
                trowlist=list('<tr>')
                for item in row:
                    trowlist.append('<td>'+str(item)+'</td>')
                trow=''.join(trowlist)
                trowlist.append('</tr>')
                tbodylist.append(trow)
            tbody=''.join(tbodylist)
            table='<table border=1>'+thead+tbody+'</table>'
            return table

	def to_json(self):
		pass
		
