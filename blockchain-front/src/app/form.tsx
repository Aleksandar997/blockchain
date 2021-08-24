import React, { Component } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TablePagination from '@material-ui/core/TablePagination';
import TableRow from '@material-ui/core/TableRow';
import * as menuOptions from "./routing.json";


// function createData(name, code, population, size) {
//   const density = population / size;
//   return { name, code, population, size, density };
// }

// const rows = [
//   createData('India', 'IN', 1324171354, 3287263),
//   createData('China', 'CN', 1403500365, 9596961),
//   createData('Italy', 'IT', 60483973, 301340),
//   createData('United States', 'US', 327167434, 9833520),
//   createData('Canada', 'CA', 37602103, 9984670),
//   createData('Australia', 'AU', 25475400, 7692024),
//   createData('Germany', 'DE', 83019200, 357578),
//   createData('Ireland', 'IE', 4857000, 70273),
//   createData('Mexico', 'MX', 126577691, 1972550),
//   createData('Japan', 'JP', 126317000, 377973),
//   createData('France', 'FR', 67022000, 640679),
//   createData('United Kingdom', 'GB', 67545757, 242495),
//   createData('Russia', 'RU', 146793744, 17098246),
//   createData('Nigeria', 'NG', 200962417, 923768),
//   createData('Brazil', 'BR', 210147125, 8515767),
// ];


export class FormProps {
  menuCode: string = '';
  // page: number = 0;
  // rowsPerPage: number = 10;
}

export class FormState {
  page: number = 0;
  rowsPerPage: number = 10;
}

export class Form extends Component<any, any> {
  columns = new Array<any>();
  constructor(props: any) {
    super(props);
    this.columns = menuOptions.menus.find(m => m.code == props.menuCode)?.columns as any;
    // this.state = new FormState();
    this.state = {
      page: 0,
      rowsPerPage: 10
    }
  }

  useStyles = makeStyles({
    root: {
      width: '100%',
    },
    container: {
      maxHeight: 440,
    },
  });

  classes = this.useStyles();
  render() {
    return (
      <Paper className={this.classes.root}>
        <TableContainer className={this.classes.container}>
          <Table stickyHeader aria-label="sticky table">
            <TableHead>
              <TableRow>
                {this.columns.map((column: any) => (
                  <TableCell
                    key={column.id}
                    align={column.align}
                    style={{ minWidth: column.minWidth }}
                  >
                    {column.label}
                  </TableCell>
                ))}
              </TableRow>
            </TableHead>
            {/* <TableBody>
                {rows.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map((row) => {
                  return (
                    <TableRow hover role="checkbox" tabIndex={-1} key={row.code}>
                      {this.columns.map((column) => {
                        const value = row[column.id];
                        return (
                          <TableCell key={column.id} align={column.align}>
                            {column.format && typeof value === 'number' ? column.format(value) : value}
                          </TableCell>
                        );
                      })}
                    </TableRow>
                  );
                })}
              </TableBody> */}
          </Table>
        </TableContainer>
        <TablePagination
          rowsPerPageOptions={[10, 25, 100]}
          component="div"
          // count={rows.length}
          count={0}
          rowsPerPage={this.state.rowsPerPage}
          page={this.state.page}
          onPageChange={(event) => this.setState({ page: event })}
          onRowsPerPageChange={(event) => this.setState({ rowsPerPage: event })}
        />
      </Paper>
    );
  }
}
