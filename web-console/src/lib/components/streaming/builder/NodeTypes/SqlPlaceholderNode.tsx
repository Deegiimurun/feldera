// The placeholder node to select a program.

import useSqlPlaceholderClick from '$lib/compositions/streaming/builder/useSqlPlaceholderClick'
import { ProgramDescr } from '$lib/services/manager'
import { PipelineManagerQuery } from '$lib/services/pipelineManagerQuery'
import React, { memo, useEffect, useState } from 'react'
import { NodeProps } from 'reactflow'

import { Autocomplete, CardContent, TextField, Typography } from '@mui/material'
import { useQuery } from '@tanstack/react-query'

import { PlaceholderNode } from '../NodeTypes'

const SqlPlaceHolderNode = (props: NodeProps) => {
  const [programs, setPrograms] = useState<ProgramDescr[]>([])
  const placeHolderReplace = useSqlPlaceholderClick(props.id)
  const onProgramSelected = (e: any, v: string) => {
    const program = programs.find(p => p.name == v)
    if (program != undefined) {
      placeHolderReplace(e, program)
    }
  }

  const { isPending, isError, data } = useQuery(PipelineManagerQuery.programs())
  useEffect(() => {
    if (!isPending && !isError) {
      setPrograms(data)
    }
  }, [isPending, isError, data])

  return (
    <PlaceholderNode>
      <CardContent sx={{ textAlign: 'center', '& svg': { mb: 2 } }}>
        {(Icon => (
          <Icon fontSize='2rem' />
        ))(props.data.icon)}
        <Typography variant='h6' sx={{ mb: 4 }}>
          {props.data.label}
        </Typography>

        <Autocomplete
          id='sql-program-select' // referenced by webui-tester
          z-index={20}
          onInputChange={onProgramSelected}
          disableCloseOnSelect
          options={programs.map(p => p.name)}
          getOptionLabel={option => option}
          renderInput={params => <TextField {...params} className='nodrag' label='Program' placeholder='Select SQL…' />}
        />
      </CardContent>
    </PlaceholderNode>
  )
}

export default memo(SqlPlaceHolderNode)
