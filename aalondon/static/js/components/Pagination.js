import React, { Component, Fragment } from 'react';
import PropTypes from 'prop-types';

class Pagination extends Component {
    componentDidMount() {
        this.gotoPage(1);
      }
    
      gotoPage = page => {
        const { onPageChanged = f => f } = this.props;
    
        const currentPage = Math.max(0, Math.min(page, this.totalPages));
    
        const paginationData = {
          currentPage,
          totalPages: this.totalPages,
          pageLimit: this.pageLimit,
          totalRecords: this.totalRecords
        };
    
        this.setState({ currentPage }, () => onPageChanged(paginationData));
      }
    
      handleClick = page => evt => {
        evt.preventDefault();
        this.gotoPage(page);
      }
    
      handleMoveLeft = evt => {
        evt.preventDefault();
        this.gotoPage(this.state.currentPage - (this.pageNeighbours * 2) - 1);
      }
    
      handleMoveRight = evt => {
        evt.preventDefault();
        this.gotoPage(this.state.currentPage + (this.pageNeighbours * 2) + 1);
      }

  constructor(props) {
    super(props);
    const { totalRecords = null, pageLimit = 30, pageNeighbours = 0 } = props;

    this.pageLimit = typeof pageLimit === 'number' ? pageLimit : 30;
    this.totalRecords = typeof totalRecords === 'number' ? totalRecords : 0;

    // pageNeighbours can be: 0, 1 or 2
    this.pageNeighbours = typeof pageNeighbours === 'number'
      ? Math.max(0, Math.min(pageNeighbours, 2))
      : 0;

    this.totalPages = Math.ceil(this.totalRecords / this.pageLimit);

    this.state = { currentPage: 1 };
  }

}

Pagination.propTypes = {
  totalRecords: PropTypes.number.isRequired,
  pageLimit: PropTypes.number,
  pageNeighbours: PropTypes.number,
  onPageChanged: PropTypes.func
};

export default Pagination;